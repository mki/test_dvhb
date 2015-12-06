from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView, RedirectView
from django.core.urlresolvers import reverse
from django.contrib.auth.views import auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import Http404

from .utils import pagination_vars
from .models import Blog, Post, Subscribe, Viewed
from .forms import PostForm, LoginForm

from braces.views import LoginRequiredMixin


class LoginView(TemplateView):
    template_name = 'login.html'

    def _get_form(self, request):
        return LoginForm(request.POST or None)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self._get_form(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['login'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('blog:blog_list'))
                else:
                    form.add_error(None, 'Пользователь не активирован')
            else:
                form.add_error(None, 'Неверный логин и/или пароль')
        context['form'] = form
        return self.render_to_response(context)



class LogoutView(RedirectView):
    pattern_name = 'blog:blog_list'

    def get(self, request, *args, **kwargs):
        auth_logout(request)

        return super(LogoutView, self).get(request, *args, **kwargs)


class PaginatedListViewMixin(View):
    template_name = ''
    page_query_param = 'p'
    template_items_var = ''

    def get(self, request):
        if self.template_items_var == '' or self.template_name == '':
            raise NotImplementedError()

        cur_page = int(request.GET.get(self.page_query_param, 1))

        context = pagination_vars(cur_page, 20, self._items(), self._url)
        context[self.template_items_var] = context['paginated_items']
        del context['paginated_items']

        return render(request, self.template_name, context)

    def _items(self):
        raise NotImplementedError()

    def _url(self, page):
        raise NotImplementedError()


class BlogListView(PaginatedListViewMixin):
    """
    У каждого пользователя есть персональный блог.
    """
    template_name = 'blog/blogs.html'
    template_items_var = 'blogs'

    def _items(self):
        return Blog.objects.all()

    def _url(self, page):
        return '/blog/view/{0}/'.format(page)


class BlogView(TemplateView):
    """
    Пост в блоге — элементарная запись с заголовком, текстом и временем создания.
    """
    template_name = 'blog/item.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        blog_id = kwargs.get('id', None)

        try:
            blog = Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            raise Http404
        else:
            context['blog'] = blog
            context['posts'] = Post.objects.filter(blog=blog)
            if request.user.is_authenticated():
                context['is_subscribed'] = Subscribe.objects.filter(
                    blog=blog,
                    user=request.user
                ).exists()
        return self.render_to_response(context)


class PostView(TemplateView):
    """
    Просмотр поста
    """
    template_name = 'blog/post.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        blog_id = kwargs.get('id', None)

        try:
            post = Post.objects.get(id=blog_id)
        except Post.DoesNotExist:
            raise Http404
        else:
            context['post'] = post

        return self.render_to_response(context)


class PostAddView(TemplateView):
    """
    Добавление поста
    """
    template_name = 'blog/add.html'

    def _get_form(self, request):
        blog_queryset = Blog.objects.filter(user=request.user)
        return PostForm(request.POST or None, blog_queryset=blog_queryset)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self._get_form(request)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = self._get_form(request)
        if form.is_valid():
            form.save()
            return redirect(reverse('blog:blog_feed'))
        context['form'] = form
        return self.render_to_response(context)


class SubscribeView(LoginRequiredMixin, RedirectView):
    """
    Пользователь может подписываться (отписываться) на блоги других пользователей (любое количество).
    """
    pattern_name = 'blog:blog_view'

    def get(self, request, *args, **kwargs):
        blog_id = kwargs.get('id', None)
        try:
            blog = Blog.objects.get(id=blog_id)
            subscribe = Subscribe.objects.filter(
                blog=blog,
                user=request.user)
        except Blog.DoesNotExist:
            raise Http404
        else:
            if subscribe.exists():
                subscribe.delete()
            else:
                Subscribe.objects.create(
                    blog=blog,
                    user=request.user)

        return super(SubscribeView, self).get(request, *args, **kwargs)


class ViewedView(LoginRequiredMixin, RedirectView):
    """
    Пользователь может помечать посты в ленте прочитанными.
    """
    pattern_name = 'blog:blog_feed'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id', None)
        try:
            post = Post.objects.get(id=post_id)
            viewed = Viewed.objects.filter(
                post=post,
                user=request.user
            )
        except Post.DoesNotExist:
            raise Http404
        else:
            if not viewed.exists():
                Viewed.objects.create(
                    post=post,
                    user=request.user)
        return redirect(reverse(self.pattern_name))


class FeedView(LoginRequiredMixin, PaginatedListViewMixin):
    """
    У пользователя есть персональная лента новостей, в которой в обратном хронологическом
    порядке выводятся посты из блогов, на которые он подписан.
    """
    template_name = 'feed/feed.html'
    template_items_var = 'posts'

    def _items(self):
        blogs = list(Subscribe.objects.filter(user=self.request.user).values_list('blog_id', flat=True))
        blogs += list(Blog.objects.filter(user=self.request.user).values_list('id', flat=True))
        viewed = Viewed.objects.filter(user=self.request.user).values_list('post_id', flat=True)
        posts = Post.objects.select_related('blog').filter(blog_id__in=blogs).order_by('-created')

        for post in posts:
            post.viewed = post.id in viewed

        return posts

    def _url(self, page):
        return '/blog/view/{0}/'.format(page)

