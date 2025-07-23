from django.contrib import admin
from .models import User,Profile,addressf,orders,orderItem
from django.contrib.auth.admin import UserAdmin



# Register your models here.

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(addressf)
admin.site.register(orders)
admin.site.register(orderItem)

def __str__(self):
    return self.username