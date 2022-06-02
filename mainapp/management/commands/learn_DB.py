from django.core.management import BaseCommand
from django.db.models import Q
from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Логическое ИЛИ
        product_1 = Product.objects.filter(
            Q(category__name='Обувь') | Q(id=11)
        )
        product_2 = Product.objects.filter(
            Q(category__name='Обувь') & Q(id=11)
        )
        product_3 = Product.objects.filter(
            ~Q(category__name='Обувь')
        )
        product_4 = Product.objects.filter(
            Q(category__name='Обувь'), id=11
        )


        print(product_1)
        print(product_2)
        print(product_3)
        print(product_4)

