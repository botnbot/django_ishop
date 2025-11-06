from django.core.management.base import  BaseCommand
from django.core.management import call_command

from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Очищает базу данных и заполняет данными из фикстуры'

    def handle(self, *args, **options):
        self.stdout.write('Очищаем базу')
        Category.objects.all().delete()
        Product.objects.all().delete()


        self.stdout.write('Загружаем данные из фикстуры')
        call_command('loaddata', 'catalog/fixtures/categories.json')
        call_command('loaddata','catalog/fixtures/products.json')
        self.stdout.write(self.style.SUCCESS('Данные из фикстур загружены'))