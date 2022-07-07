from django.db import models
from django.contrib.auth.models import AbstractUser
# Author model
from django.urls import reverse


class Author(AbstractUser):
    author_name = models.CharField(max_length=70, blank=False)
    avatar = models.ImageField(upload_to="photos/profile/%Y/%m/%d/", blank=True, verbose_name="Фото профиля")

    def get_absolute_url(self):
        return reverse('profile/accounts/', kwargs={'author_id': self.pk})