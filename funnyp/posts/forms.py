from .models import Post, Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'body')

        labels = {
            'author': 'Autor',
            'body': 'Treść',
        }


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'image', 'content', 'zajawka')
        labels = {
                'title': 'Tytuł',
                'category': 'Kategoria',
                'image': 'Zdjęcie główne',
                'content': 'Treść'
            }
        help_texts = {
                'zajawka': 'Maksymalnie 200 znaków'
        }
    
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }