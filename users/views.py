from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


from django.shortcuts import redirect


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        self.object = form.save()
        user_email = self.object.email

        login(self.request, self.object)

        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию на сайте!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            "Регистрация прошла успешно! На вашу почту отправлено приветственное письмо."
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        print("FORM INVALID:", form.errors)
        return super().form_invalid(form)



# ------------------ Вход ------------------ #
class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, f"Вы успешно вошли как {form.get_user().email}")
        return super().form_valid(form)


# ------------------ Выход ------------------ #
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:product_list")

    def post(self, request, *args, **kwargs):
        messages.success(request, "Вы вышли из аккаунта")
        return super().post(request, *args, **kwargs)


# ------------------ Редактирование профиля ------------------ #
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("catalog:product_list")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён")
        return super().form_valid(form)
