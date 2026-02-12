from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView

from catalog.forms import ProductForm, ContactForm
from catalog.models import Product, Category
from catalog.services import get_products_from_cache, get_products_by_category


class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.owner or self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "Редактировать продукт может только владелец")
        return redirect("catalog:product_list")


class OwnerOrProductModeratorRequiredMixin(UserPassesTestMixin):
    """Владелец или член группы 'Модератор продуктов'"""

    def test_func(self):
        obj = self.get_object()
        user = self.request.user

        if user == obj.owner:
            return True

        return user.groups.filter(name="Модератор продуктов").exists()

    def handle_no_permission(self):
        messages.error(self.request, "Доступно только владельцу или модератору продуктов")
        return redirect("catalog:product_list")


class ProductsListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"

    def get_queryset(self):
        user = self.request.user
        products = get_products_from_cache()

        if not user.is_authenticated:
            return products.filter(status=Product.STATUS_PUBLISHED)

        if user.is_staff or user.has_perm("catalog.can_unpublish_product"):
            return products

        return (
                products.filter(status=Product.STATUS_PUBLISHED)
                | products.filter(owner=user)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        for product in context['products']:
            product.can_edit = user.is_authenticated and (
                    user == product.owner or user.is_staff)  # владелец или staff

            product.can_delete = (
                    user.is_authenticated and (
                    user == product.owner
                    or user.is_staff
                    or user.has_perm("catalog.can_delete_product")
            )
            )

            product.can_unpublish = (user.is_authenticated
                                     and user.has_perm('catalog.can_unpublish_product')
                                     and product.status == Product.STATUS_PUBLISHED
                                     )  # право can_unpublish_product
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

        context['can_edit'] = (
                user.is_authenticated and (
                user == product.owner or user.is_staff))
        context['can_delete'] = (
                user.is_authenticated
                and (user == product.owner or user.is_staff))
        context['can_publish'] = (
                user.is_authenticated
                and user.has_perm('catalog.can_publish_product')
                and product.status != Product.STATUS_PUBLISHED
        )
        context["can_unpublish"] = (
                user.is_authenticated
                and user.has_perm("catalog.can_unpublish_product")
                and product.status == Product.STATUS_PUBLISHED
        )

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


class ProductsUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:product_list")


class ProductsDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView
):
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    context_object_name = "product"
    success_url = reverse_lazy("catalog:product_list")

    def test_func(self):
        product = self.get_object()
        user = self.request.user

        return (
                user == product.owner
                or user.is_staff
                or user.has_perm("catalog.can_unpublish_product")
        )

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления")
        return redirect("catalog:product_list")


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "catalog.can_unpublish_product"

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.status == Product.STATUS_PUBLISHED:
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


class CategoryProductsListView(ListView):
    model = Product
    template_name = "catalog/category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return get_products_by_category(category_id=self.category.pk,
                                        user=self.request.user
                                        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ContactsView(FormView):
    template_name = "catalog/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form):
        messages.success(self.request, "Сообщение успешно отправлено")
        return super().form_valid(form)
