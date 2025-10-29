from django.urls import path
from catalog.apps import CatalogConfig
# from catalog import home
from catalog.views import home, contacts

# app_name = 'catalog'

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name='home'),
    path("contacts", contacts, name='contacts'),
]
