from django.utils import timezone

from django.conf import settings
from django.db import models


class Product(models.Model):
    STATUS_PENDING = "pending"
    STATUS_PUBLISHED = "published"
    STATUS_UNPUBLISHED = "unpublished"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Ожидает модерации"),
        (STATUS_PUBLISHED, "Опубликован"),
        (STATUS_UNPUBLISHED, "Снят с публикации"),
    ]

    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Изображение",
        null=True,
        blank=True,
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    created_at = models.DateTimeField(
        auto_now=True
    )
    updated_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        permissions = [
            ("can_unpublish_product", "Может снимать продукт с публикации"),
            ("can_publish_product", "Может публиковать продукт"),
        ]

    def __str__(self):
        return self.name

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED



class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.name} {self.description}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]
