import json
import datetime
import os
from django.conf import settings

from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from store.models import *
from store.utils import  cookieCart, cartData, guestOrder, get_protocol
from store.forms import UserCreationForm

from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def store(request):
    data = cartData(request)
    
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def detail(request, id):
    data = cartData(request)
    
    cartItems = data['cartItems']

    product = Product.objects.get(pk=id)

    context = { "product": product, 'cartItems': cartItems }
    return render(request, 'store/detail.html', context)
    

def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'order': order, 'items': items, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    clientID = settings.YOUR_CLIENT_ID
    
    context = {
        'order': order, 
        'items': items, 
        'cartItems': cartItems, 
        'YOUR_CLIENT_ID': clientID,
        'YOUR_FROM_WHERE_ARE': 'USD' # order.get_cart_items_currency
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(pk=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=0)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False, transaction_id=0)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )
        processOrderEmail(request, customer)

    return JsonResponse('Payment submitted..', safe=False)

def processOrderEmail(request, customer):
    username = customer.user.username
    email = customer.email
   
    print(username)
    print(email)
    
    template = render_to_string('store/checkout_email.html', {})
    
    email = EmailMessage(
        'Thanks for your purchase!!',
        template,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = False
    email.send()


def signIn(request):

    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)
           
            if user is not None:
                login(request, user)
                return redirect('store')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context = { "pub_date": datetime.datetime.now() }
    return render(request, 'accounts/login.html', context)


def signOut(request):
    logout(request)
    return redirect('store')


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            registerEmail(request)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def registerEmail(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    domain = get_current_site(request)
    protocol = get_protocol(request)

    template = render_to_string('accounts/register_email.html', {
        'name': username,
        'domain': domain,
        'protocol': protocol
        })
    
    email = EmailMessage(
        'Thanks for signing up!!',
        template,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = False
    email.send()