
from django.core.exceptions import DisallowedHost
from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
from ecommerce.util import *

# class Brand(models.Model):
#     title = models.CharField(max_length=100)
#     image = models.ImageField(null=True,blank=True)

#     def str(self):
#         return self.title
#     @property
#     def imageURL(self):
#         try:
#             url = self.image.url
#         except:
#             url = " "
#         return url

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    description = models.CharField(max_length=500,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    size = models.IntegerField(null=True, blank=True)
    colour = models.CharField(max_length=200, null=True,blank=True)
    # category = models.CharField(max_length=200, null=True)
    # brand = models.ForeignKey(Brand, on_delete=models.CASCADE ,default=1)
    # @staticmethod
    # def get_all_brand():
    #     Product.objects.filter()

    def __str__(self):
        return self.name


    def get_sale(self):
    #"'Calculate cost with the discount"'
        disprice = float(self.price * 20 / 100)
        after_discount = float(self.price - disprice)
        return after_discount

    def get_sale50(self):
    #"'Calculate cost with the discount"'
        disprice = float(self.price * 50 / 100)
        after_discount = float(self.price - disprice)
        return after_discount

    def rec(self):
        objs = Product.get(name="Jordan Delta 2")
    
    # @staticmethod
    # def get_all_products_by_brandid(brand_id):
    #     if brand_id:
    #         return Product.objects.filter(brand = brand_id)
    #     else:
    #         return Product.objects.all()

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = " "
        return url

class Images(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(null=True,blank=True)

    def str(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = " "
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        
    @property
    def shipping(self):
        shipping = True
        orderitems = self.orderitem_set.all()
        return shipping

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    # size = models.ForeignKey(Size, on_delete=models.CASCADE,blank = True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    pincode = models.CharField(max_length=200,null=True)
    mobile = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

@receiver(pre_save, sender=Product)
def pre_save_receiver(sender, instance, *args, **kwargs):
   if not instance.slug:
       instance.slug = unique_slug_generator(instance)    


class Footer(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.title
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = " "
        return url


# class Size(models.Model):
#      title = models.CharField(max_length=200, null=True)

# class Category(models.Model):



class Carousel(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.title
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = " "
        return url


