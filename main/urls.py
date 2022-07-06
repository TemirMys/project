from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_post/', Add_post.as_view(), name='add_post'),
    path('hot_posts/', Hot_posts, name ='hot_posts'),
    path('categories/', Categories, name='categories'),
    path('register/', Register, name='register'),
    path('login/', Login, name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('comment/<int:post_id>/', Comments, name='comment' ),
    path('like/<int:post_id>', LikeView, name='like_post'),
]