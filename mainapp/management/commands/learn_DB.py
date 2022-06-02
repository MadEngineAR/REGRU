from django.core.management import BaseCommand
import json
from abc import ABC

from django.db.models import Q
from mainapp.models import Product, ProductCategories
from authapp.models import User


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



        print(product_1)
        print(product_2)
        print(product_3)

