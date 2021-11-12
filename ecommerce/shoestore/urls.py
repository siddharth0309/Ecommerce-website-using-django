from django.urls.conf import include
from . import views
from django.urls import path
urlpatterns = [
    path('',views.home,name="home"),
    path('cart/',views.cart,name="cart"),
    path('products/',views.products,name="products"),
    path('checkout/',views.checkout,name="checkout"),
    path('products/<slug:slug>',views.productdetail,name="productdetail"),
    path('offers/',views.offers,name="offers"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('search/', views.searchBar, name='search'),
    
]