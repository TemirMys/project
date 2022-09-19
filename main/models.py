from django.db import models
from django.urls import reverse

from Author.models import Author
from autoslug import AutoSlugField

# Post model
class Post(models.Model):
    title = models.CharField(max_length=165, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True, unique_with='pub_date', verbose_name="URL")
    content = models.TextField(max_length=20000, verbose_name="Текст статьи")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Фото")
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории")
    rating = models.ManyToManyField(Author, related_name='like_postm', blank=True)
    author_name = models.ForeignKey(Author,
                                    on_delete=models.CASCADE,

                                    verbose_name='Имя автора')
    def total_rating(self):
        return self.rating.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def image_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return 'static/main/images/no_image.jpg'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id']

# Comment model
class Comment(models.Model):
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Имя автора')
    comment = models.TextField(max_length=2000)
    date_create = models.DateTimeField(auto_now=True, verbose_name='Время создания комментария')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment', verbose_name='id Поста')

    def __str__(self):
        return f'Comment for {self.post_id}'

    def get_absolute_url(self):
        return reverse('comment', kwargs={'post_id': self.post_id})