from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from catalog.forms import ProductForm, ContactForm
from catalog.models import Product



class ProductModerationMixin(PermissionRequiredMixin):
    """Миксин для пользователей с правом can_unpublish_product"""
    permission_required = "catalog.can_unpublish_product"
    raise_exception = False

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("catalog:products_list")


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Владелец продукта или модератор с правом can_unpublish_product"""
    def test_func(self):
        obj = self.get_object()
        return (
            self.request.user == obj.owner or
            self.request.user.has_perm("catalog.can_unpublish_product") or
            self.request.user.is_staff
        )

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("catalog:products_list")


class StaffRequiredMixin(UserPassesTestMixin):
    """Проверка, что пользователь staff"""
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


class ProductsCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        # Автоматически назначаем владельца продукта
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт создан и ожидает модерации")
        return super().form_valid(form)


class ProductsUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    """Редактирование доступно владельцу или модератору"""
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:products_list")


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    """Удаление доступно владельцу, модератору или staff"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:products_list")


class ProductUnpublishView(LoginRequiredMixin, ProductModerationMixin, UpdateView):
    """Снять публикацию продукта может модератор"""
    model = Product
    fields = ["status"]
    template_name = "catalog/product_unpublish.html"
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        form.instance.status = "unpublished"
        messages.success(self.request, f"Продукт '{form.instance.name}' снят с публикации")
        return super().form_valid(form)



class ContactsView(LoginRequiredMixin, FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно отправлено")
        return super().form_valid(form)
