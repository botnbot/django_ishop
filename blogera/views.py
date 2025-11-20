from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from blogera.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blogera/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailsView(DetailView):
    model = Post
    template_name = 'blogera/post_details.html'
    context_object_name = 'post'


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blogera/confirm_post_delete.html'
    success_url = reverse_lazy('blogera:post_list')
    context_object_name = 'post'


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blogera/post_create.html'
    success_url = reverse_lazy('blogera:post_list')
    context_object_name = 'post'


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image']
    template_name = 'blogera/post_update.html'
    success_url = reverse_lazy('blogera:post_list')
    context_object_name = 'post'
