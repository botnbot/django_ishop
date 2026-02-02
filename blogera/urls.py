from django.urls import path
from blogera.views import (
    PostListView,
    PostDetailsView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostUnpublishView,
)

app_name = "blogera"

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailsView.as_view(), name="post_details"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("post/<int:pk>/unpublish/", PostUnpublishView.as_view(), name="post_unpublish"),
]
