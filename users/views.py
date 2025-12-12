from django.core.mail import send_mail

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.conf import settings
from .forms import CustomUserCreationForm


class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        user_email = (
            self.object.email
        )

        send_mail(
            subject="Добро пожаловать!",
            message="Спасибо за регистрацию на сайте!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
        )

        return response
