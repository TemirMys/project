from django.db.models import Count

from .models import *

menu = [{'title': "Главная страница", 'url_name': "home"},
        {'title': "Добавить пост", 'url_name' : "add_post"},
        {'title': 'Горячее', 'url_name' :'hot_posts'},
        {'title': 'Категории', 'url_name' : 'categories'}
        ]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        context['menu'] = user_menu
        context['comment'] = Comment.objects.all()
        context['posts'] = Post.objects.all()

        return context
