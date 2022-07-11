from django.urls import path, include
from .views import *
from Author.models import Author


urlpatterns = [
    path('', include(router.urls)),
    path('drf-auth/', include('rest_framework.urls'))
]