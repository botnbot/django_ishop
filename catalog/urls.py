from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ProductDetailsView, ContactsView, ProductsCreateView, ProductsUpdateView, ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='product_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('product/new/', ProductsCreateView.as_view(), name='products_create'),
    path('products/<int:pk>/edit/', ProductsUpdateView.as_view(), name='products_update'),
    path('product_details/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    path('contacts/', ContactsView.as_view(), name='contacts'),
]
