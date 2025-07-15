from django.contrib import admin
from EApp.models import *

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display= ['id', 'name', 'description', 'price', 'in_stock']
    list_filter = ('in_stock',)

class SignupAdmin(admin.ModelAdmin):
    list_display= ['id', 'name', 'email', 'phone', 'is_admin']

class CartItemAdmin(admin.ModelAdmin):
    list_display= ['product', 'quantity', 'user', 'date_added']

class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display= ['name', 'phone', 'pincode', 'house', 'area', 'landmark', 'city', 'state']

class PaymentAdmin(admin.ModelAdmin):
    list_display= ['user', 'amount', 'payment_status', 'transaction_id', 'timestamp']

class OrderListAdmin(admin.ModelAdmin):
    list_display= ['id', 'user', 'delivery_address', 'payment', 'expected_delivery_date', 'created_at', 'status']

admin.site.register(ProductModel, ProductAdmin)
admin.site.register(SignupModel, SignupAdmin)
admin.site.register(CartItemModel, CartItemAdmin)
admin.site.register(DeliveryAddressModel, DeliveryAddressAdmin)
admin.site.register(PaymentModel, PaymentAdmin)
admin.site.register(OrderModel, OrderListAdmin)