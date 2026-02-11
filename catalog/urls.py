from django.urls import path
from django.views.decorators.cache import cache_page
from catalog import views
from catalog.models import Category
from catalog.views import CategoryProductsListView

app_name = "catalog"

urlpatterns = [
    path("", views.ProductsListView.as_view(), name="product_list"),  # список продуктов
    path("product/<int:pk>/", cache_page(10) (views.ProductDetailView.as_view()), name="product_detail"),  # детали продукта
    path("product/create/", views.ProductsCreateView.as_view(), name="product_create"),  # создать продукт
    path("product/<int:pk>/update/", views.ProductsUpdateView.as_view(), name="product_update"),  # редактировать продукт
    path("product/<int:pk>/delete/", views.ProductsDeleteView.as_view(), name="product_delete"),  # удалить продукт
    path("contacts/", views.ContactsView.as_view(), name="contacts"),  # контакты
    path("product/<int:pk>/unpublish/", views.ProductUnpublishView.as_view(), name="product_unpublish"), # Снять продукт с публикации
    path("product/<int:pk>/publish/", views.ProductPublishView.as_view(), name="product_publish"), # Опубликовать продукт
    path("category/<int:pk>", CategoryProductsListView.as_view(), name='category_products',),
]


