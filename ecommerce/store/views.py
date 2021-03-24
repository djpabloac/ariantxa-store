from django.shortcuts import render
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
<<<<<<< HEAD
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    context = {'order': order, 'items': items}
=======

    context = {'items': items}
>>>>>>> 81b92c7d038d4be2aa81698bf5d5bfe9bba59fe4
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, create = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        customer = {}
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}

    context = {'customer': customer, 'order': order, 'items': items}
    return render(request, 'store/checkout.html', context)