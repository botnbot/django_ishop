from django.db import models

from config import settings


class Product(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает модерации"),
        ("published", "Опубликован"),
        ("unpublished", "Снят с публикации"),
    ]
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/", verbose_name="Изображение", null=True, blank=True
    )
    category = models.ForeignKey(
        to="Category",
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="products",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="цена за покупку"
    )
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateField(auto_now=True, verbose_name="Дата изменения")
    is_published = models.BooleanField(default=False,verbose_name="Опубликован")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")

    class Meta:
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
        ]

    def __str__(self):
        return f"{self.name} {self.description}"


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]
