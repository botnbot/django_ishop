from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=False)
    avatar = forms.ImageField(required=False)
    country = forms.CharField(max_length=50, required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "username",
            "avatar",
            "country",
            "phone_number",
            "password1",
            "password2",
        )
