from django.core.management.base import BaseCommand
from shop.models import cart,cartItem
from datetime import datetime, timedelta
from django.utils import timezone

class command(BaseCommand):

    help = 'delete old carts'

    def handle(self,*args,**kargs):

        threshold = timezone.now() - timedelta(days=10)
        
        user_cart = cart.objects.filter(created_date=threshold,user__isnull = True)
        user_items = cartItem.objects.filter(cart=user_cart)

        user_cart.delete()
        user_items.delete()

        self.stdout.write('Successfully deleted old carts and items.')

