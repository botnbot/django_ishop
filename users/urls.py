from django.urls import path
from . import views
from .views import CustomLogoutView

app_name = "users"
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path('register/', views.RegisterView.as_view(), name='register'),
]
