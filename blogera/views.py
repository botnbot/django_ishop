from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from blogera.models import Post


class PostListView(ListView):
    model = Post
    fields = ['title','created_at']
    template_name = 'blogera/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailsView(DetailView):
    model = Post
    template_name = 'blogera/post_details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

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
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blogera/post_update.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blogera:post_details', kwargs={'pk': self.object.pk})
