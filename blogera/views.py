from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blogera/confirm_post_delete.html'
    success_url = reverse_lazy('blogera:post_list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blogera/post_create.html'
    success_url = reverse_lazy('blogera:post_list')
    context_object_name = 'post'

    def form_valid(self, form):
        form.instance.author = self.request.user  # автоматически назначает автора посту
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blogera/post_update.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse_lazy('blogera:post_details', kwargs={'pk': self.object.pk})

    def test_func(self):
        """Проверяет, что пользователь автор поста или админ."""
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
