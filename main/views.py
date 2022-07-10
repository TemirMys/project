from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import DataMixin
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from Author.forms import AuthorCreationFrom
from django.core.paginator import Paginator

# Like post button
def LikeView(request, post_id):
    post = get_object_or_404(Post, id=request.POST.get('post_like'))
    post.rating.add(request.user)
    return HttpResponseRedirect(reverse('post', kwargs={'post_slug': post.slug}))

#Hot posts
class HotPostsView(DataMixin, ListView):
    model = Post
    context_object_name = 'posts'
    slug_url_kwarg = 'post_slug'
    template_name = 'main/hot.html'


    def get_queryset(self):
        #return Post.objects.order_by('-rating').filter(is_published=True).distinct()

        return Post.objects.raw(
            'Select main_post.*, main_post_rating.id as likes from main_post inner join main_post_rating on (main_post.id = main_post_rating.post_id) where main_post.is_published = True group by main_post.id order by count(main_post_rating.id) desc'
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Популярные посты")
        return dict(list(context.items()) + list(user_context.items()))



#Category all
class CategoriesView(DataMixin, ListView):
    model = Category
    template_name = 'main/all_categories.html'
    context_object_name = 'categories'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все категории')
        context['posts'] = Post.objects.all()
        return dict(list(context.items()) + list(c_def.items()))


#Category filter
class CategoryFilterView(DataMixin, ListView):
    model = Category
    template_name = 'main/category.html'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'

    def get_queryset(self):
        return Category.objects.filter(slug=self.kwargs['category_slug']).distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryFilterView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(**kwargs)
        context['category'] = Category.objects.filter(slug=self.kwargs['category_slug'])
        context['post'] = Post.objects.filter(is_published = True, category=context['category'][0].pk)
        context['title'] = 'Категория - ' + str(context['category'][0].name)
        post = context['post']
        return dict(list(context.items()) + list(c_def.items()))


#register
class RegisterAuthor(DataMixin, CreateView):
    form_class = AuthorCreationFrom
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(user_context.items()))


#login
class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'main/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(user_context.items()))

    def get_success_url(self):
        return reverse_lazy('home')

#logout
def logout_user(request):
    logout(request)
    return redirect('home')

#comment
def Comments(request, post_id):
    posts = Post.objects.all()
    comments = Comment.objects.filter(post_id=post_id)
    return render(request, 'main/comment.html', {'posts':posts, 'comments': comments})

#add post
class Add_post(DataMixin, CreateView):
    model = Post
    template_name = 'main/add_post.html'
    form_class = AddPostForm
    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Добавить пост")
        return dict(list(context.items()) + list(user_context.items()))


#home page
class HomePageView(DataMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/home.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(user_context.items()))

    def get_queryset(self):
        return Post.objects.order_by('-pub_date').filter(is_published=True)


#Detailed view of post
class ShowPost(DataMixin, FormMixin, DetailView):
        model = Post
        template_name = 'main/post.html'
        slug_url_kwarg = 'post_slug'
        context_object_name = 'post'
        form_class = CommentForm

        def get_success_url(self):
            return reverse('post', kwargs={'post_slug': self.object.slug})

        def get_context_data(self, **kwargs):
            context = super(ShowPost, self).get_context_data(**kwargs)
            context['form'] = CommentForm(initial={'post_id': self.object})
            post_rated = get_object_or_404(Post, id=context['post'].pk)
            total_rating = post_rated.total_rating()
            context['total_rating'] = total_rating
            user_context = self.get_user_context()
            return dict(list(context.items()) + list(user_context.items()))


        def form_valid(self, form):
            form.instance.author_name = self.request.user
            form.instance.post_id = self.object
            form.save()
            return super(ShowPost, self).form_valid(form)

        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
