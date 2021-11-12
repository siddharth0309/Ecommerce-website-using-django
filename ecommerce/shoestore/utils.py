import json
from .models import *


#Functions For Guest User
def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total':0,'get_cart_items':0,'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'price':product.price,
                    'name':product.name,
                    'imageURL':product.imageURL, 
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)
            order['shipping'] = True
        except:
            pass
    return {'items':items,'order':order,'cartItems':cartItems}

def cartData(request): 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items'] 
    return {'items':items,'order':order,'cartItems':cartItems}