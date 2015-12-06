from django import forms
from .models import Post, Blog


class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        blog_queryset = kwargs.pop('blog_queryset')

        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['blog'] = forms.ModelChoiceField(
                required=False, queryset=blog_queryset)

    class Meta:
        model = Post
        fields = ['blog', 'title', 'content']


class LoginForm(forms.Form):
    """
    Форма логина для неавторизированного пользователя.
    """
    login = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')
