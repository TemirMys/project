from django import forms
from .models import *

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo', 'is_published', 'category']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
