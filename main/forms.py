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

#class AuthorRegistrationForm(forms.ModelForm):
 #   class Meta:
  #      model = Author
   #     fields = ['username', 'password1', 'password2', 'author_name']