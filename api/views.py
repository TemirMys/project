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
from rest_framework.mixins import CreateModelMixin


#general viewset
class PostViewSet(viewsets.ModelViewSet, CreateModelMixin):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAdminOrReadOnly]



    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     elif self.request.method == 'POST':
    #         return [IsAuthenticatedOrReadOnly()]
    #     elif self.request.method == 'PUT':
    #         return [IsAuthorOrReadOnly()]
    #     elif self.request.method == 'DELETE':
    #         return [IsAdminOrReadOnly()]
    #     return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if not pk:
            return Post.objects.all()

        return Post.objects.filter(pk=pk)

    @action(methods=['get'], detail=True) #category by it's category_id
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.name})


    @action(methods=['post', 'get'], detail=True,
            permission_classes = [IsAuthenticatedOrReadOnly],
            serializer_class = CommentSerializer)
    def post_comment(self, request, pk=None):
        if request.method == "POST":
            serializer = self.get_serializer_class(data = request.data)
        if request.method == "GET":
            comment = Comment.objects.get(pk=pk)
            return Response({'comment': comment.comment})



#
# #commentaries viewset
# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return Comment.objects.all()
#
#         return Comment.objects.filter(pk=pk)
#
#     @action(methods=['post'], detail=True) #category by it's category_id
#     def comment(self, request, pk=None):
#         comment = Comment.objects.get(pk=pk)
#         return Response({'comment': comment.comment})

#
# class Comment2ViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = (IsAuthenticatedOrReadOnly, )





router = routers.DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
# router.register(r'post-comment', Comment2ViewSet)



# Create your views here.
