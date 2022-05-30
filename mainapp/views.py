from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from pathlib import Path

from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from mainapp.models import Product, ProductCategories

BASE_DIR = Path(__file__).resolve().parent.parent


# Create your views here.


def index(request):
    content = {'title': 'geekshop Store'}
    return render(request, 'mainapp/index.html', content)


# @cache_page(3600)
# def products(request, id_category=None, page=1):
#     if id_category:
#         products_ = Product.objects.filter(category_id=id_category).select_related()
#         cancel = 'Сбросить фильтр'  # необходимо для того, чтобы "Cбросить фильтр" появлялся только при
#         # выборе  категории, а не на главной."
#         categories = ProductCategories.objects.filter(id=id_category).select_related()  # В шаблоне отображается только одна выбранная
#         # категория
#     else:
#         products_ = Product.objects.filter(is_active=True)  # Чтобы в пагинатор не попали неактивные продукты(удаленные)
#         categories = ProductCategories.objects.all()
#         cancel = None
#     pagination = Paginator(products_, per_page=2)
#     try:
#         product_pagination = pagination.page(page)
#     except PageNotAnInteger:
#         product_pagination = pagination.page(1)
#     except EmptyPage:
#         product_pagination = pagination.page(pagination.num_pages)
#
#     content = {'title': 'geekshop - Каталог',
#                'products': product_pagination,
#                'categories': categories,
#                'cancel': cancel
#                }
#     return render(request, 'mainapp/products.html', content)

def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategories.objects.all()
            cache.set(key, link_category)
            return link_category
    else:
        return ProductCategories.objects.all()


def get_link_product(category, page):
    if settings.LOW_CACHE:
        if category:
            key = f'link_product{category}{page}'
            link_product = cache.get(key)
            if link_product is None:
                link_product = Product.objects.filter(category_id=category).select_related('category')
                cache.set(key, link_product)
                return link_product
        else:
            key = 'link_product'
            link_product = cache.get(key)
            if link_product is None:
                link_product = Product.objects.filter(is_active=True).select_related('category')  # Чтобы в пагинатор
                # не попали неактивные продукты(удаленные)
                cache.set(key, link_product)
                return link_product
    else:
        return Product.objects.filter(is_active=True).select_related('category')  # Чтобы в пагинатор
        # не попали неактивные продукты(удаленные)


def get_product_(pk):
    if settings.LOW_CACHE:
        key = 'product'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
            return product
    else:
        return Product.objects.get(id=pk)


# @cache_page(3600)
def products(request, id_category=None, page=1):
    if id_category:
        # products_ = Product.objects.filter(category_id=id_category).select_related()
        products_ = get_link_product(id_category, page)
        cancel = 'Сбросить фильтр'  # необходимо для того, чтобы "Cбросить фильтр" появлялся только при
        # выборе  категории, а не на главной."
        # categories = ProductCategories.objects.filter(id=id_category).select_related()  # В шаблоне
        # отображается только одна выбранная категория
    else:
        products_ = get_link_product(None, None)
        # categories = ProductCategories.objects.all()
        cancel = None
        pagination = Paginator(products_, per_page=2)
    try:
        product_pagination = pagination.page(page)
    except PageNotAnInteger:
        product_pagination = pagination.page(1)
    except EmptyPage:
        product_pagination = pagination.page(pagination.num_pages)

    content = {'title': 'geekshop - Каталог',
               'products': product_pagination,
               # 'categories': categories,
               'categories': get_link_category(),
               'cancel': cancel
               }
    return render(request, 'mainapp/products.html', content)


class ProductDetail(DetailView):
    model = Product
    template_name = 'mainapp/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data()
        context['product'] = get_product_(self.kwargs.get('pk'))
        return context
