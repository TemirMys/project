from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Author

class AuthorCreationFrom(UserCreationForm):
    class Meta:
        model = Author
        fields = ['username', 'password1', 'password2', 'author_name', 'avatar']
