from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from catalog.models import Product
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" с нужными правами'

    def handle(self, *args, **kwargs):
        # Создаем группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем контент-тайп для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Назначаем права: добавление, изменение и удаление продукта
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_unpublish_product', 'delete_product']
        )
        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS('Разрешения назначены успешно'))
