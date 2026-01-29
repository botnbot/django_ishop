from django.urls import path
from catalog import views

app_name = "catalog"

urlpatterns = [
    path("", views.ProductsListView.as_view(), name="products_list"),
    path("product/<int:pk>/", views.ProductDetailsView.as_view(), name="product_details"),
    path("product/create/", views.ProductsCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", views.ProductsUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", views.ProductsDeleteView.as_view(), name="product_delete"),
    path("contacts/", views.ContactsView.as_view(), name="contacts"),
]
