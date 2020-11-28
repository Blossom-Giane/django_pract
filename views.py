from django.shortcuts import render, get_object_or_404
from .models import post
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (ListView,
                                 DetailView,
                                 CreateView,
                                 UpdateView,
                                 DeleteView,
                                 )

#me = redirect_to_login('next')
def  home(request):
    context = {
        'posts': post.objects.all()
    }
    return render(request, 'blog_app/home.html', context)

class PostListView(ListView):
    model = post
    template_name = 'blog_app/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = post
    template_name = 'blog_app/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return post.objects.filter(author=user).order_by('-date_posted')

class PostDetaiLView(DetailView):
    model = post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     UpdateView):
    model = post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,
                     UserPassesTestMixin,
                     DeleteView):
    model = post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog_app/about.html', {'title': 'About'})

# Create your views here.