from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from django.conf import settings
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# ------------------ Регистрация ------------------ #
class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        user_email = self.object.email

        # Отправка приветственного письма
        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию на сайте!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
        )

        # Автоматический вход пользователя после регистрации
        login(self.request, self.object)

        # Сообщение на сайте
        messages.success(
            self.request,
            "Регистрация прошла успешно! На вашу почту отправлено приветственное письмо."
        )
        return response


# ------------------ Вход ------------------ #
class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def form_valid(self, form):
        messages.success(self.request, f"Вы успешно вошли как {form.get_user().username}")
        return super().form_valid(form)


# ------------------ Выход ------------------ #
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("catalog:products_list")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы вышли из аккаунта")
        return super().dispatch(request, *args, **kwargs)


# ------------------ Редактирование профиля ------------------ #
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("catalog:products_list")

    def get_object(self, queryset=None):
        # Возвращаем текущего пользователя
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль успешно обновлён")
        return super().form_valid(form)
