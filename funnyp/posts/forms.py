from .models import Post, Comment
from django import forms
from crispy_forms.helper import FormHelper

class CommentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.fields['body'].widget.attrs['rows'] = 1

    class Meta:
        model = Comment
        fields = ('body',)

        labels = {
            'body': '',
        }


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'zajawka')
        labels = {
                'title': 'Tytuł',
                'category': 'Kategoria',
                'content': 'Treść'
            }
        help_texts = {
                'zajawka': 'Maksymalnie 200 znaków'
        }