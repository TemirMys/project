from django.contrib import admin
from .models import Author
from .forms import AuthorCreationFrom
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = Author
    add_form = AuthorCreationFrom

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Author',
            {
                'fields': (
                    'author_name',
                    'avatar',
                )
            }
        )
    )
admin.site.register(Author, CustomUserAdmin)
