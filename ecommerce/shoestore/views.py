from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .models import Footer
from django.http import JsonResponse
import json
import datetime
from .utils import cartData
from .models import Carousel
# from .models import Brand
#import requests
# Create your views here.
def products(request):
    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    # brand = Brand.objects.all()
    context={
        'products':products,
        'cartItems':cartItems,
        # 'brand' : brand
    }
    return render(request,'ecommerce/products.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'ecommerce/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context={
        'items':items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request,'ecommerce/checkout.html',context)
def home(request):
    data = cartData(request)
    cartItems = data['cartItems']
    carousel = Carousel.objects.all()
    footer = Footer.objects.all()
    context={
        'footer': footer,
        'cartItems':cartItems,
        'carousel':carousel
    }
    return render(request,'ecommerce/home.html',context)    


def productdetail(request,slug):
    data = cartData(request)
    cartItems = data['cartItems']
    xtraimg = Images.objects.all()
    q = Product.objects.filter(slug__iexact = slug)
    #sizes = Size.objects.all()

    if q.exists():
       q = q.first()
    else:
       return HttpResponse('<h1>Page Not Found</h1>')
    context = {
       'product': q,
       #'sizes': sizes,
       'cartItems':cartItems,
       'xtraimg':xtraimg
    }
    return render(request,'ecommerce/productdetail.html',context)




def offers(request):
    products = Product.objects.all()
    context={
        'products':products
    }
    return render(request,'ecommerce/offers.html',context) 


def updateItem(request):
    #data = requests.get('/update_item/').json()
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ',action)
    print('productId: ',productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer , complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order , product=product)

    if action == 'add':
        orderItem.quantity = ( orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = ( orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def processOrder(request):
    tranasaction_id = datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer , complete=False)
        total =float(data['form']['total'])    
        order.transaction_id = tranasaction_id
    
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
                pincode=data['shipping']['pincode'],
            )
    else:
        print("User is not logged in")
    return JsonResponse('Payment complete',safe=False)


def searchBar(request):
    data = cartData(request)
    cartItems = data['cartItems']
    

    products = Product.objects.all()
    context={
        'products':products,
        'cartItems':cartItems
    }

    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            products = Product.objects.filter(name__icontains=query) 
            return render(request, 'ecommerce/searchbar.html', {'products':products})
        else:
            print("No information to show")
            return render(request, 'searchbar.html', {})

