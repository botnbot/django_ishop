from django.contrib import admin

from blogera.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "is_published",
        "views_count",
    )
    list_filter = ("created_at", "is_published")
    search_fields = ("title",)


