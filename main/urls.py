from django.urls import path
from .views import *
from Author.models import Author

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('add_post/', Add_post.as_view(), name='add_post'),
    path('all_categories/', CategoriesView.as_view(), name='all_categories'),
    path('register/', RegisterAuthor.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('comment/<int:post_id>/', Comments, name='comment' ),
    path('like/<int:post_id>', LikeView, name='like_post'),
    path('category/<slug:category_slug>', CategoryFilterView.as_view(), name='category'),
    path('hot', HotPostsView.as_view(), name='hot'),
    path('logout', logout_user, name='logout')
]