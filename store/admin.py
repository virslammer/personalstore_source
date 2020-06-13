from django.contrib import admin
from .models import Customer, Product, Order, OrderItem,ShippingAddress, Category, Ads
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    pass
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','order','quantity','date_added']

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem,OrderItemAdmin)
admin.site.register(ShippingAddress)
admin.site.register(Ads)