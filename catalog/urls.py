from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductsListView, ProductDetailsView, ContactsView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductsListView.as_view(), name='product_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('product_details/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
]
