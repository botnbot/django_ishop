from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    content = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to="blog/images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    is_published = models.BooleanField(default=False, verbose_name="Опубликован")

    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Счетчик просмотров"
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )

    def __str__(self):
        return f"{self.title} ({self.created_at:%d.%m.%Y})"

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ["-created_at"]
        permissions = [
            ("can_unpublish_post", "Может снимать пост с публикации"),
        ]

