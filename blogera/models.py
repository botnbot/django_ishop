from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.created_at.strftime('%d.%m.%Y')})"

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ["-created_at"]
