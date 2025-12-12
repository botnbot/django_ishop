from django.urls import path

from blogera.apps import BlogeraConfig
from blogera.views import (
    PostListView,
    PostDetailsView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

app_name = BlogeraConfig.name

urlpatterns = [
    path("post_list/", PostListView.as_view(), name="post_list"),
    path("post_details/<int:pk>/", PostDetailsView.as_view(), name="post_details"),
    path("post_create/", PostCreateView.as_view(), name="post_create"),
    path("post_update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("post_delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
]
