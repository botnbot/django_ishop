from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
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
    """Автор поста или модератор"""

    def test_func(self):
        obj = self.get_object()
        return (
                self.request.user == obj.author
                or self.request.user.has_perm("blogera.can_unpublish_post")
                or self.request.user.is_staff
        )

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("blogera:post_list")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blogera/post_form.html"
    success_url = reverse_lazy("blogera:post_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Пост создан и ожидает модерации")
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = "blogera/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            return Post.objects.filter(is_published=True) | Post.objects.filter(author=user)

        return Post.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        for post in context["posts"]:
            post.can_edit = (
                    user.is_authenticated
                    and (user == post.author or user.is_staff or user.has_perm("blogera.can_unpublish_post"))
            )
            post.can_delete = user.is_authenticated and (user == post.author or user.is_staff)

            post.can_publish = (
                    user.is_authenticated
                    and user.has_perm("blogera.can_publish_post")
                    and not post.is_published
            )

            post.can_unpublish = (
                    user.is_authenticated
                    and user.has_perm("blogera.can_unpublish_post")
                    and post.is_published
            )

        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "blogera/post_details.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        post = super().get_object(queryset)

        if post.is_published:
            return post

        if (
                self.request.user == post.author
                or self.request.user.has_perm("blogera.can_unpublish_post")
                or self.request.user.is_staff
        ):
            return post

        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        post = self.object

        post.can_edit = (
                user.is_authenticated
                and (user == post.author or user.is_staff or user.has_perm("blogera.can_unpublish_post"))
        )

        post.can_delete = user.is_authenticated and (user == post.author or user.is_staff)

        post.can_unpublish = (
                user.is_authenticated
                and user.has_perm("blogera.can_unpublish_post")
                and post.is_published
        )

        post.can_publish = (
                user.is_authenticated
                and user.has_perm("blogera.can_publish_post")
                and not post.is_published
        )

        return context


class PostUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blogera/post_form.html"
    success_url = reverse_lazy("blogera:post_list")


class PostDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    model = Post
    template_name = "blogera/post_confirm_delete.html"
    success_url = reverse_lazy("blogera:post_list")


class PostUnpublishView(LoginRequiredMixin, PostModerationMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.is_published = False
        post.save(update_fields=["is_published"])

        messages.success(request, f"Пост «{post.title}» снят с публикации")
        return redirect("blogera:post_list")


class PostPublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "blogera.can_publish_post"

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        if post.is_published:
            messages.info(request, "Пост уже опубликован")
            return redirect("blogera:post_list")

        post.is_published = True
        post.save(update_fields=["is_published"])

        messages.success(request, f"Пост «{post.title}» опубликован")
        return redirect("blogera:post_list")
