from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from Author.models import Author
from main.models import Post, Category, Comment
from rest_framework import routers
from .permissions import *
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


#general viewset
class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthenticatedOrReadOnly()]
        elif self.request.method == 'PUT':
            return [IsAuthorOrReadOnly()]
        elif self.request.method == 'DELETE':
            return [IsAdminOrReadOnly()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Post.objects.all()

        return Post.objects.filter(pk=pk)

    @action(methods=['get'], detail=True) #category by it's category_id
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.name})


#commentaries viewset
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Comment.objects.all()

        return Comment.objects.filter(pk=pk)

    @action(methods=['post'], detail=True) #category by it's category_id
    def comment(self, request, pk=None):
        comment = Comment.objects.get(pk=pk)
        return Response({'comment': comment.comment})





router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet)



# Create your views here.
