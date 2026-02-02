from django import forms
from blogera.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "is_published",
        ]
