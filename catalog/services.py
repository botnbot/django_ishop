from django.core.cache import cache
from django.db.models import Q

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_from_cache():
    if not CACHE_ENABLED:
        return Product.objects.all()

    key = "product_list_ids"
    product_ids = cache.get(key)

    if product_ids is None:
        product_ids = list(
            Product.objects.values_list("id", flat=True)
        )
        cache.set(key, product_ids, timeout=60)

    return Product.objects.filter(id__in=product_ids)


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
