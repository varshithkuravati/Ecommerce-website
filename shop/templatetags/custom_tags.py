from django import template
from shop.models import cart,cartItem

register = template.Library()

@register.filter

def times(value):
    value = int(value)
    return range(value)

@register.filter

def rating(value):
    if value > 0:
        value = int(value)
        return 5-int(value)
    else:
        return 0
    
@register.filter
    
def upper(value):
    if value:
        return value.upper()
    

@register.simple_tag(takes_context=True)

def cart_count(context):
    
    req = context.get('request')

    if req.user:

        if req.user.is_authenticated:
            
            user_cart,bl = cart.objects.get_or_create(user=req.user)
            cart_items = cartItem.objects.filter(cart=user_cart)
            cart_counts = cart_items.count()

            return cart_counts
    

    session_id = req.session.session_key

    cart_counts = 0

    if session_id:
        
        try:
             
             user_cart = cart.objects.get(session_id=session_id)
             cart_items = cartItem.objects.filter(cart=user_cart)
             cart_counts = cart_items.count()
        except cart.DoesNotExist:

            cart_counts = 0


    

    

    return cart_counts

