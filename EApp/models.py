from django.db import models

# Create your models here.

class ProductModel(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField(null=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True, verbose_name="In Stock")
    image= models.ImageField(upload_to='products/')

class SignupModel(models.Model):
    name= models.CharField(max_length=64)
    email= models.EmailField()
    phone= models.CharField(max_length=15)
    password= models.CharField(max_length=128)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class CartItemModel(models.Model):
    product= models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=0, null=True)
    user= models.ForeignKey(SignupModel, on_delete=models.CASCADE)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} {self.product.name}'
    
class DeliveryAddressModel(models.Model):
    name= models.CharField(max_length=64)
    phone= models.CharField(max_length=15)
    pincode= models.CharField(max_length=7)
    house= models.CharField(max_length=100)
    area= models.CharField(max_length=100)
    landmark= models.CharField(max_length=100)
    city= models.CharField(max_length=100)
    state= models.CharField(max_length=100)

class PaymentModel(models.Model):
    user = models.ForeignKey(SignupModel, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')  # or 'Success', 'Failed'
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_status} - {self.transaction_id}"
    
class OrderModel(models.Model):
    user= models.ForeignKey(SignupModel, on_delete=models.CASCADE)
    delivery_address= models.ForeignKey(DeliveryAddressModel, on_delete=models.SET_NULL, null=True)
    payment= models.OneToOneField(PaymentModel, on_delete=models.CASCADE)
    expected_delivery_date= models.DateField()
    created_at= models.DateTimeField(auto_now_add=True)
    status= models.CharField(max_length=20, default="Processing")

    def __str__(self):
        return f"order #{self.id} by {self.user}"
