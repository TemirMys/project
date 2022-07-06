from django.db import models
from django.urls import reverse

from Author.models import Author
from autoslug import AutoSlugField

# Post model
class Post(models.Model):
    title = models.CharField(max_length=165, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True,
                         unique_with='pub_date', verbose_name="URL")
    content = models.TextField(max_length=20000, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    rating = models.ManyToManyField(Author, related_name='blog_posts')
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Имя автора')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['pub_date']

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True,
                         unique_with='pub_date', verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# Comment model
class Comment(models.Model):
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Имя автора')
    comment = models.TextField(max_length=2000)
    date_create = models.DateTimeField(auto_now=True, verbose_name='Время создания комментария')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='id Поста')

