from django.db import models
from django.contrib.auth.models import AbstractUser

# from shop.models import products

# Create your models here.


class User(AbstractUser):
    email = models.EmailField('email address',unique=True)
    # username = models.CharField(max_length=100,default=None)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    name = models.CharField(max_length=500)
    # photo = models.ImageField(upload_to='static/images',blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phonenum = models.CharField(max_length=100,blank=True)


    def __str__(self):
        return self.user.username
    

class addressf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True,blank=True,default="")
    phonenum = models.CharField(max_length=100,blank=True,null=True,default="")
    houseNo = models.CharField(max_length=100,null=True,blank=True,default="")
    address = models.CharField(max_length=500,null=True,blank=True,default="")
    city = models.CharField(max_length=100,null=True,blank=True,default="")
    state = models.CharField(max_length=100,null=True,blank=True,default="")
    country = models.CharField(max_length=100,null=True,blank=True,default="")
    pincode = models.CharField(max_length=20,null=True,blank=True,default="")

    def __str__(self):
        return f"{self.user.username} - {self.address}"
    

class orders(models.Model):

    status_choices = [
        ('payment pending','Payment Pending'),
        ('processing','processing'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('cancelled','cancelled'),
        ('returned','returned'),
        ('replaced','replaced'),

        
    ]

    type_choices = [

        ('order','order'),
        ('return','return'),
        ('replace','replace'),
        ('cancel','cancel'),


    ]





    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    order_id = models.CharField(max_length=255, unique=True, blank=True)
    Odate = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='payment pending',choices=status_choices)
    location = models.CharField(max_length=255, blank=True)
    order_tracking = models.CharField(max_length=255,blank=True)
    type = models.CharField(max_length=255,blank=True,default="order",choices=type_choices)
    reason = models.CharField(max_length=255,blank=True)
    est_dates = models.JSONField(null=True)
    payment_id = models.CharField(max_length=255, blank=True)

class orderItem(models.Model):
    product = models.ForeignKey('shop.products',on_delete=models.CASCADE,default=1)
    order = models.ForeignKey(orders,related_name='order_item',on_delete=models.CASCADE,default=1)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.ForeignKey('shop.colors', on_delete=models.CASCADE, blank=True,default=1)
    size = models.ForeignKey('shop.sizes', on_delete=models.CASCADE, blank=True,default=1)

    def get_total(self):
        return self.product.price*self.quantity

    




