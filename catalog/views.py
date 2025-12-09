from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductsCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_staff


class ProductsUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        if form.cleaned_data.get('image-clear') and form.instance.image:
            form.instance.image.delete(save=False)
            form.instance.image = None
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

class ProductsListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'


class ProductDetailsView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_details.html'
    form_class = ProductForm
    context_object_name = 'product'


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        return self.request.user.is_staff


class ContactsView(LoginRequiredMixin,View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо, {name}! Ваше сообщение получено.")
