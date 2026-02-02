from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogera.forms import PostForm
from blogera.models import Post


class PostModerationMixin(PermissionRequiredMixin):
    """Миксин для пользователей с правом can_unpublish_post"""
    permission_required = "blogera.can_unpublish_post"
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("blogera:post_list")


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Владелец поста или модератор с правом can_unpublish_post"""

    def test_func(self):
        obj = self.get_object()
        return (
                self.request.user == obj.author or
                self.request.user.has_perm("blogera.can_unpublish_post") or
                self.request.user.is_staff
        )

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("blogera:post_list")


class PostListView(ListView):
    model = Post
    template_name = "blogera/post_list.html"
    context_object_name = "posts"


class PostDetailsView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blogera/post_details.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blogera/post_form.html"
    success_url = reverse_lazy("blogera:post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Пост создан и ожидает модерации")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blogera/post_form.html"
    success_url = reverse_lazy("blogera:post_list")


class PostDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Post
    template_name = "blogera/post_confirm_delete.html"
    success_url = reverse_lazy("blogera:post_list")


class PostUnpublishView(
    LoginRequiredMixin,
    PostModerationMixin,
    View
):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        post.is_published = False
        post.save()

        messages.success(
            request,
            f"Пост «{post.title}» снят с публикации"
        )
        return redirect("blogera:post_list")
