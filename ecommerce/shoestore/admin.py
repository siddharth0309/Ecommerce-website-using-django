from django.contrib import admin
from .models import *

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 4

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [ProductImageInline]

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Footer)
admin.site.register(Carousel)
admin.site.register(Images)
# admin.site.register(Brand)
