from django.conf.urls import url

from blog.views import (
    BlogListView, BlogView, FeedView, SubscribeView, ViewedView, PostView, PostAddView,
    LogoutView, LoginView
)


urlpatterns = [
    url(r'^$', BlogListView.as_view(), name='blog_list'),
    url(r'^view/blog/(?P<id>\d+)/$', BlogView.as_view(), name='blog_view'),
    url(r'^view/post/(?P<id>\d+)/$', PostView.as_view(), name='post_view'),
    url(r'^add/$', PostAddView.as_view(), name='post_add'),
    url(r'^subscribe/(?P<id>\d+)/$', SubscribeView.as_view(), name='subscribe_view'),
    url(r'^viewed/(?P<id>\d+)/$', ViewedView.as_view(), name='viewed_view'),
    url(r'^feed/$', FeedView.as_view(), name='blog_feed'),
    url(r'^logout/$', LogoutView.as_view(), name='blog_logout'),
    url(r'^login/$', LoginView.as_view(), name='blog_login'),
]
