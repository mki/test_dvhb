from django.db import models
from django.db.models.signals import pre_delete, post_save

from django.dispatch.dispatcher import receiver

from django.contrib.auth.models import User

from datetime import datetime as dt

from .utils import _send_email


class Blog(models.Model):
    user = models.ForeignKey(User)
    name = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    blog = models.ForeignKey(Blog)
    title = models.TextField(default='', blank=True)
    content = models.TextField(default='', blank=True)
    created = models.DateTimeField(default=dt.now)

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    blog = models.ForeignKey(Blog, db_index=True)
    user = models.ForeignKey(User, db_index=True)


class Viewed(models.Model):
    post = models.ForeignKey(Post, db_index=True)
    user = models.ForeignKey(User, db_index=True)


@receiver(pre_delete, sender=Subscribe, dispatch_uid='viewed_pre_delete')
def viewed_pre_delete_handler(sender, instance, **kwargs):
    """
    При удалении подписки пометки о "прочитанности" сохранять не нужно
    """
    if kwargs.get('raw'):
        return
    Viewed.objects.filter(post_id__in=Post.objects.filter(blog=instance.blog)).delete()


@receiver(post_save, sender=Post, dispatch_uid='post_post_save')
def post_post_save_handler(sender, instance, created, **kwargs):
    """
    При добавлении поста в ленту — подписчики получают почтовое уведомление со ссылкой на новый пост.
    """
    if kwargs.get('raw'):
        return
    if created:
        subs = Subscribe.objects.select_related('user').filter(blog=instance.blog)
        for sub in subs:
            # TODO refactoring to Celery task for emailing
            _send_email(sub.user.email, instance.id)


