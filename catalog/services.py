from itertools import product

from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    """Получение продуктов из кэша, если кэш пуст - получение из базы"""
    if not CACHE_ENABLED == True:
        return Product.objects.all()
    key = 'product_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products, timeout=10)
    return products


from django.db.models import Q
from catalog.models import Product


def get_products_by_category(category_id, user=None):
    """
    Возвращает список продуктов по категории
    с учетом прав доступа.
    """

    chosen_products = Product.objects.filter(category_id=category_id)

    # Аноним
    if not user or not user.is_authenticated:
        return chosen_products.filter(status=Product.STATUS_PUBLISHED)

    # Staff или модератор
    if user.is_staff or user.has_perm("catalog.can_unpublish_product"):
        return chosen_products

    # Обычный пользователь
    return chosen_products.filter(
        Q(status=Product.STATUS_PUBLISHED) | Q(owner=user)
    ).distinct()
