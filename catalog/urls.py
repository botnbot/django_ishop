from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import contacts, product_details, product_list


app_name = CatalogConfig.name

urlpatterns = [
    path("contacts/", contacts, name="contacts"),
    path("", product_list, name="product_list"),
    path("product_details/<int:pk>/", product_details, name="product_details"),
]
