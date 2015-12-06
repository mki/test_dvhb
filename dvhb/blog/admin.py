from django.contrib import admin

from blog.models import Blog, Post


class BlogAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
    list_display = ['name', 'user']


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    ordering = ['created']
    list_display = ['title', 'created', 'blog']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
