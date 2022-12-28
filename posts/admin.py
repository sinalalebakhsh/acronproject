from django.contrib import admin

from .models import Post, Comment



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'text', 'datetime_created', )


@admin.register(Post)
class BookAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'cover', )



