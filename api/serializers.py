from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from main.models import Post, Category, Comment


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = ('id', 'author_name', 'title', 'content', 'is_published', 'category')

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = ('author_name', 'post_id', 'comment', )