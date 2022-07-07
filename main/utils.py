from django.db.models import Count

from .models import *

menu = [{'title': "Главная страница", 'url_name': "home"},
        {'title': "Добавить пост", 'url_name' : "add_post"},
        {'title': 'Горячее', 'url_name' :'hot'},
        {'title': 'Категории', 'url_name' : 'all_categories'}
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['comment'] = Comment.objects.all()
        context['category'] = Category.objects.all()

        return context
