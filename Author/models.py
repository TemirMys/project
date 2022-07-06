from django.db import models
from django.contrib.auth.models import AbstractUser
# Author model

class Author(AbstractUser):
    author_name = models.CharField(max_length=70)
    avatar = models.ImageField(upload_to="photos/profile/%Y/%m/%d/", blank=True, verbose_name="Фото профиля")
