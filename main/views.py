from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, FormView
from .utils import DataMixin
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin


def LikeView(request, post_id):
    post = get_object_or_404(Post, id=request.POST.get('post_like'))
    post.rating.add(request.user)
    return HttpResponseRedirect(reverse('post', kwargs={'post_slug': post.slug}))

def Hot_posts(request):
    return HttpResponse('Hot posts page')

def Categories(request):
    return HttpResponse('Categories page')

def Register(request):
    return HttpResponse('Register page')

def Login(request):
    return HttpResponse('Login page')

#comment
def Comments(request, post_id):
    posts = Post.objects.all()
    comments = Comment.objects.filter(post_id=post_id)
    return render(request, 'main/comment.html', {'posts':posts, 'comments': comments})

#add post
class Add_post(CreateView):
    model = Post
    template_name = 'main/add_post.html'
    form_class = AddPostForm
    def form_valid(self, form):
        form.instance.author_name = self.request.user
        return super().form_valid(form)







#home page
class HomePageView(DataMixin, ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'main/home.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        menu = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(menu.items()))

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


#Detailed view of post
class ShowPost(FormMixin, DetailView):
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
            return context



        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

        def form_valid(self, form):
            form.instance.author_name = self.request.user
            form.instance.post_id = self.object
            form.save()
            return super(ShowPost, self).form_valid(form)
