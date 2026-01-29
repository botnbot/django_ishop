from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from blogera.models import Post


class AuthorOrStaffMixin(UserPassesTestMixin):
    """Миксин для проверки прав: автор или staff"""
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("blogera:post_list")


class PostListView(ListView):
    model = Post
    template_name = "blogera/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by("-created_at")


class PostDetailsView(DetailView):
    model = Post
    template_name = "blogera/post_details.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        # инкрементируем счетчик просмотров оптимально
        Post.objects.filter(pk=self.object.pk).update(views_count=self.object.views_count + 1)
        return self.object


class PostDeleteView(LoginRequiredMixin, AuthorOrStaffMixin, DeleteView):
    model = Post
    template_name = "blogera/confirm_post_delete.html"
    success_url = reverse_lazy("blogera:post_list")
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image", "is_published"]
    template_name = "blogera/post_create.html"
    success_url = reverse_lazy("blogera:post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, AuthorOrStaffMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "is_published"]
    template_name = "blogera/post_update.html"
    context_object_name = "post"

    def get_success_url(self):
        return reverse_lazy("blogera:post_details", kwargs={"pk": self.object.pk})
