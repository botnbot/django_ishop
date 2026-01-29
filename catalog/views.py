from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from catalog.forms import ProductForm, ContactForm
from catalog.models import Product


class StaffRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь является staff"""
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("catalog:products_list")


class ProductsListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_details.html"
    context_object_name = "product"


class ProductsCreateView(LoginRequiredMixin, StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")


class ProductsUpdateView(LoginRequiredMixin, StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:products_list")


class ContactsView(LoginRequiredMixin, FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно отправлено")
        return super().form_valid(form)
