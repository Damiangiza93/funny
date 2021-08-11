from django.contrib import admin
from .models import Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'date_posted')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'body', 'date_added')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category)