from django.db import models
from django.conf import settings

from django.utils.text import slugify

from django.utils import timezone
# from users.models import orders

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category')

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    

class brands(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(Category,blank=True)



    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
    
    def __str__(self):
        return self.name


class colors(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(Category,blank=True)



    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
    
    def __str__(self):
        return self.name

class sizes(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)



    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
    
    def __str__(self):
        return self.name




class products(models.Model):



    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True,null=True,blank=True)
    shortdesc = models.CharField(max_length=200,blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    rating = models.IntegerField(null=True)
   
    # image = models.ImageField(upload_to='products',blank=True)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE,default=1,null=True)
    brand = models.ForeignKey(brands,on_delete=models.CASCADE,default=1,null=True)
    Color = models.ManyToManyField(colors,blank=True)
    size = models.ManyToManyField(sizes,blank=True)

    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        
        self.slug = slugify(self.name)



        super().save(*args, **kwargs)



    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
    
class ratings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,default=1)
    product = models.ForeignKey(products,related_name="ratings",on_delete=models.CASCADE,default=1)
    orderitem = models.ForeignKey('users.orderItem',on_delete=models.CASCADE,null=True)
    value = models.IntegerField(default=0)
    description = models.TextField(default='')
    date = models.DateField(auto_now=True)

    



    
class productImg(models.Model):
    product = models.ForeignKey(products,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products',blank=True)


class ratingImg(models.Model):
    
    rating = models.ForeignKey(ratings,related_name="images",on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ratings',blank=True)

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        images = ratingImg.objects.filter(rating=self.rating).order_by('pk')

        if images.count() > 4:

            old_images = images[:images.count()-4]
            for img in old_images:
                img.image.delete(save=False)
                img.delete()

class cart(models.Model):
    session_id = models.CharField(max_length=255,unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_date']

class cartItem(models.Model):
    cart = models.ForeignKey(cart,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)
    color = models.ForeignKey(colors, on_delete=models.CASCADE, blank=True,default=1)
    size = models.ForeignKey(sizes, on_delete=models.CASCADE, blank=True,default=1)
    
    def get_total(self):
        return self.product.price*self.quantity
    

class coupons(models.Model):
    code = models.CharField(max_length=255,unique=True)
    discount_type = models.CharField(max_length=100,choices=(('percentage','Percentage'),('fixed','Fixed Amount')))
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    usage_limit = models.PositiveIntegerField(default=1)
    per_user_limit = models.PositiveIntegerField(default=1)

    def is_valid(self,user=None):

        now = timezone.now()

        if not self.active:
            return False
        
        if self.valid_from > now or self.valid_to < now:
            return False
        
        if self.usage_limit > 0 and self.usages.count() >= self.usage_limit:
            return False
        
        if user:
            if self.per_user_limit > 0 and self.usages.filter(user=user).count() >= self.per_user_limit:
                return False
            
        return True
    
    def __str__(self):
        return self.code


class couponUsages(models.Model):
    coupon = models.ForeignKey(coupons,related_name='usages',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    used_at = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey('users.orders',on_delete=models.CASCADE,null=True)
    discount = models.DecimalField(max_digits=10,decimal_places=2,null=True)

    def __str__(self):
        return self.coupon






    

    


    





