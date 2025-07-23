from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .views import get_session_id
from .models import cartItem,cart
# from ecom.middleware.store_old import get_old_key

from django.core.cache import cache


def do_transfer(req,user):
   
   #  user = req.user

    session_id = cache.get(f"old_session")

    print(session_id)

    if not session_id:
        session_id = ''

    try:
       
       session_cart = cart.objects.get(session_id=session_id)

    except cart.DoesNotExist:
       
       session_cart = None
       
    try:

       user_cart = cart.objects.get(user=user)

    except cart.DoesNotExist:
       
        user_cart = None

    
    if user_cart:

        session_items = cartItem.objects.filter(cart=session_cart)

        for item in session_items:

           cart_item = cartItem.objects.get(cart=user_cart,product=item.product,color=item.color,size=item.size)

           if cart_item:

            cart_item.quantity += item.quantity
            cart_item.save()

           else:

                new_item = cartItem.objects.create(
                cart = user_cart,
                product = item.product,
                quantity = item.quantity,
                color = item.color,
                size = item.size
                )
            
                new_item.save()

        if session_cart:
           
           if session_items:
              session_items.delete()

           session_cart.delete()

           cache.delete(f"old_session")
           


    else:
       
        if session_cart:
          
          session_cart.user = user
          session_cart.session_id = ''
          session_cart.save()

          

          cache.delete(f"old_session")



   
   
   

@receiver(user_logged_in)

def transfer(sender, request, user, **kwargs):

    do_transfer(request,user)