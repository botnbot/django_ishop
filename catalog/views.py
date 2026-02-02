from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
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
        return redirect("catalog:product_list")


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
        return redirect("catalog:product_list")


class StaffRequiredMixin(UserPassesTestMixin):
    """Проверка, что пользователь staff"""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для этого действия")
        return redirect("catalog:product_list")


class ProductsListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.filter(
                status=Product.STATUS_PUBLISHED
            ) | Product.objects.filter(owner=user)
        return Product.objects.filter(status=Product.STATUS_PUBLISHED)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        for product in context['products']:
            product.can_edit = user.is_authenticated and (
                    user == product.owner or user.is_staff or user.has_perm('catalog.can_unpublish_product'))
            product.can_delete = user.is_authenticated and (user == product.owner or user.is_staff)
            product.can_unpublish = user.is_authenticated and user.has_perm('catalog.can_unpublish_product')
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        product = super().get_object(queryset)

        if product.status == Product.STATUS_PUBLISHED:
            return product

        if (
            self.request.user == product.owner
            or self.request.user.has_perm("catalog.can_unpublish_product")
            or self.request.user.is_staff
        ):
            return product

        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user

        context['can_publish'] = user.is_authenticated and user.has_perm('catalog.can_publish_product') and product.status != Product.STATUS_PUBLISHED
        context['can_edit'] = user.is_authenticated and (user == product.owner or user.is_staff or user.has_perm('catalog.can_unpublish_product'))
        context['can_delete'] = user.is_authenticated and (user == product.owner or user.is_staff)
        context['can_unpublish'] = user.is_authenticated and user.has_perm('catalog.can_unpublish_product') and product.status == Product.STATUS_PUBLISHED

        return context



class ProductsCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")

    def form_valid(self, form):
        # Автоматически назначаем владельца продукта
        form.instance.owner = self.request.user
        messages.success(self.request, "Продукт создан и ожидает модерации")
        return super().form_valid(form)


class ProductsUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductsDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    """Удаление доступно владельцу, модератору или staff"""
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        product.status = Product.STATUS_UNPUBLISHED
        product.save(update_fields=["status"])

        messages.success(request, "Продукт снят с публикации")
        return redirect("catalog:product_list")


class ProductPublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_publish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.status = Product.STATUS_PUBLISHED
        product.save(update_fields=["status"])
        messages.success(request, "Продукт опубликован")
        return redirect("catalog:product_list")


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно отправлено")
        return super().form_valid(form)
