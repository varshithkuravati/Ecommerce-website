from django.contrib import admin
from .models import products,Category,productImg,brands,colors,sizes,ratings,cart,cartItem,coupons,couponUsages

# Register your models here.

class productImgAdmin(admin.TabularInline):
    model = productImg
    extra = 1
    fields = ['image',]
    max_num = 10

class productsAdmin(admin.ModelAdmin):
    inlines = [productImgAdmin]



admin.site.register(products,productsAdmin)
admin.site.register(Category)
admin.site.register(brands)
admin.site.register(colors)
admin.site.register(sizes)
admin.site.register(cart)
admin.site.register(cartItem)
admin.site.register(ratings)
admin.site.register(coupons)
admin.site.register(couponUsages)


