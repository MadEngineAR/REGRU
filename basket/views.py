from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models import F

from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from mainapp.models import Product
from basket.models import Basket


# @login_required
# def basket_add(request, id):
#     user_select = request.user
#     product = Product.objects.get(id=id)
#     baskets = Basket.objects.filter(user=user_select, product=product)
#
#     if baskets:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#     else:
#         Basket.objects.create(user=user_select, product=product, quantity=1)
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#
#
# @login_required
# def basket_remove(request, basket_id):
#     Basket.objects.get(id=basket_id).delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def basket_add(request, id, page=2):
    if request.is_ajax():
        user_select = request.user
        product = Product.objects.get(id=id)
        baskets = Basket.objects.filter(user=user_select, product=product)

        if baskets:
            basket = baskets.first()
            # basket.quantity += 1
            basket.quantity = F('quantity') + 1
            basket.save()

            update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
            print(update_queries)
        else:
            Basket.objects.create(user=user_select, product=product, quantity=1)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, basket_id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=basket_id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

    baskets = Basket.objects.filter(user=request.user)
    context = {'baskets': baskets}
    result = render_to_string('basket/basket.html', context)
    return JsonResponse({'result': result})
