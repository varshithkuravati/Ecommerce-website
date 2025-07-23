from django.shortcuts import render,redirect
from .models import products,Category,productImg,brands,colors,sizes,cart,cartItem,coupons,couponUsages,ratings
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.db.models import Q

from django.template.loader import render_to_string
from django.http import JsonResponse
from users.forms import addressForm

from users.models import addressf

# Create your views here.


def index(req):

    pr = products.objects.prefetch_related('images').all().filter(available = True)
    cat = Category.objects.all()
    
    pag_cat = Paginator(cat,4)
    pag_pr = Paginator(pr,4)

    page_pr = 1
  
    pr1 = pag_pr.page(page_pr)
    cat1 = pag_cat.page(page_pr)

     


    context = {
        'products': pr1,
        'categories': cat1
    }

    return render(req,'shop/index.html',context)

def category(req,slug):
    
    # type = req.POST.get(category)
    type = Category.objects.get(slug=slug)
    pr = products.objects.prefetch_related("ratings").all().filter(available = True,Category=type)
    cat = Category.objects.all()
    bnd = brands.objects.all().filter(category=type)
    colr = colors.objects.all().filter(category=type)
    sz = sizes.objects.all().filter(category=type)


    


    if req.method == "POST":
        pr = products.objects.prefetch_related('images').all()

        Brands = req.POST.getlist('brands[]')
        Sizes = req.POST.getlist('sizes[]')
        Colors = req.POST.getlist('colors[]')
        categories = req.POST.getlist('categories[]')
        selected = req.POST.get('selected')

        q = Q()
        if Brands:
            

            for brand in Brands:
                q = q | Q(brand__name__iexact=brand)
            
            pr = pr.filter(q).distinct()

            q = Q()

        if Sizes:

            for size in Sizes:
                q =  q | Q(size__name__iexact=size)

            pr = pr.filter(q).distinct()

            q = Q()

        if Colors:

            for color in Colors:
                q =  q | Q(Color__name__iexact=color)

            pr = pr.filter(q).distinct()

            q = Q()

        
        if categories:

            for category in categories:
                q =  q | Q(Category__name=category)

            pr = pr.filter(q)

            q = Q()
        

        if selected:
            if selected == "low":
                pr = pr.order_by('price')
            if selected == "high":
                pr = pr.order_by('-price')
            if selected == "rated":
                pr = pr.order_by('-rating')
            if selected == "new":
                pr = pr.order_by('-pk')


        pag_pr = Paginator(pr,4)

        try:
          pr_num  = req.POST.get('page')
        except:
          pr_num = 1

        if pr_num == None:
            pr_num = 1
    
        pr1 = pag_pr.page(pr_num)

        context = {
        'products': pr1,
        'categories': cat,
        'pc': type.slug,
         }

        
        html = render_to_string('shop/product_list.html',context)

        return JsonResponse({'html':html})
        
            




    pag_pr = Paginator(pr,4)

    try:
        pr_num  = req.GET.get('page')
    except:
        pr_num = 1

    if pr_num == None:
        pr_num = 1
    
    pr1 = pag_pr.page(pr_num)

    context = {
        'products': pr1,
        'categories': cat,
        'brands': bnd,
        'colors': colr,
        'sizes': sz,
        'pc': type.slug,
    }

    return render(req,'shop/category.html',context)


def search(req,slug):
    
    # type = req.POST.get(category)
    # type = Category.objects.get(slug=slug)
    pr = products.objects.prefetch_related("ratings").all().filter(available = True)

    slug = slug.replace("-"," ").title()

    q1 = Q()

    q1 = Q(name__iregex=fr'{slug}') | Q(description__iregex=fr'{slug}') | Q(shortdesc__iregex=fr'{slug}')

    pr = pr.filter(q1)


    cat = Category.objects.all()
    bnd = brands.objects.all()
    colr = colors.objects.all()
    sz = sizes.objects.all()


    


    if req.method == "POST":
        pr = products.objects.prefetch_related('images').all().filter(q1)

        Brands = req.POST.getlist('brands[]')
        Sizes = req.POST.getlist('sizes[]')
        Colors = req.POST.getlist('colors[]')
        categories = req.POST.getlist('categories[]')
        selected = req.POST.get('selected')

        q = Q()
        if Brands:
            

            for brand in Brands:
                q = q | Q(brand__name__iexact=brand)
            
            pr = pr.filter(q).distinct()

            q = Q()

        if Sizes:

            for size in Sizes:
                q =  q | Q(size__name__iexact=size)

            pr = pr.filter(q).distinct()

            q = Q()

        if Colors:

            for color in Colors:
                q =  q | Q(Color__name__iexact=color)

            pr = pr.filter(q).distinct()

            q = Q()

        
        if categories:

            for category in categories:
                q =  q | Q(Category__name=category)

            pr = pr.filter(q)

            q = Q()
        

        if selected:
            if selected == "low":
                pr = pr.order_by('price')
            if selected == "high":
                pr = pr.order_by('-price')
            if selected == "rated":
                pr = pr.order_by('-rating')
            if selected == "new":
                pr = pr.order_by('-pk')


        pag_pr = Paginator(pr,4)

        try:
          pr_num  = req.POST.get('page')
        except:
          pr_num = 1

        if pr_num == None:
            pr_num = 1
    
        pr1 = pag_pr.page(pr_num)

        context = {
        'products': pr1,
        'categories': cat,
        'pc': type,
         }

        
        html = render_to_string('shop/product_list.html',context)

        return JsonResponse({'html':html})
        
            




    pag_pr = Paginator(pr,4)

    try:
        pr_num  = req.GET.get('page')
    except:
        pr_num = 1

    if pr_num == None:
        pr_num = 1
    
    pr1 = pag_pr.page(pr_num)

    context = {
        'products': pr1,
        'categories': cat,
        'brands': bnd,
        'colors': colr,
        'sizes': sz,
        'pc': slug,
    }

    return render(req,'shop/search.html',context)








def pds(req):
   pr = products.objects.prefetch_related('images').all().filter(available=True)
   cat = Category.objects.all()

   pag_pr = Paginator(pr,6)

   page = 1

   try:
      page = req.GET.get('page')

   except:
       page = 1

   
   if page==None:
       page=1
   

  
   
   
   pr1 = pag_pr.page(page)

   context = {
       
       'products': pr1,
       'categories': cat
   }

   return render(req,'shop/products.html',context) 



def cts(req):
   pr = products.objects.prefetch_related('images').all().filter(available=True)
   cat = Category.objects.all()

   pag_cat = Paginator(cat,6)

   page = 1

   if req.method == "GET":

   
       page = req.GET.get('page')

    
   if page == None:
       page =1
  
   
    
   
   cat1 = pag_cat.page(page)

   context = {
       
       'products': pr,
       'categories': cat1
   }

   return render(req,'shop/categories.html',context)



def productDetail(req,slug):
    
    product = products.objects.get(slug=slug)
    image = productImg.objects.all().filter(product=product)
    cat = Category.objects.all()
    clrs = product.Color.all()
    sz = product.size.all()
    Rproducts = products.objects.prefetch_related('images').filter(Category = product.Category).exclude(id=product.id)



    rating = ratings.objects.filter(product=product).order_by('-date')


    avg_scr = 0

    for r in rating:
        avg_scr += r.value

    avg_scr = avg_scr / rating.count() if rating.count() > 0 else 0

    rating_count = rating.count()

    rating_5_count = rating.filter(value=5).count()
    rating_4_count = rating.filter(value=4).count()
    rating_3_count = rating.filter(value=3).count()
    rating_2_count = rating.filter(value=2).count()
    rating_1_count = rating.filter(value=1).count()

    per_5 = ((rating_5_count / rating_count) * 100) if rating_count > 0 else 0
    per_4 = ((rating_4_count / rating_count) * 100) if rating_count > 0 else 0
    per_3 = ((rating_3_count / rating_count) * 100) if rating_count > 0 else 0
    per_2 = ((rating_2_count / rating_count) * 100) if rating_count > 0 else 0
    per_1 = ((rating_1_count / rating_count) * 100) if rating_count > 0 else 0

    ratings_data = {

        'avg_scr': avg_scr,
        'total_count': rating_count,
        'rating_5_count': rating_5_count,
        'rating_4_count': rating_4_count,
        'rating_3_count': rating_3_count,
        'rating_2_count': rating_2_count,
        'rating_1_count': rating_1_count,
        'per_5': per_5,
        'per_4': per_4,
        'per_3': per_3,
        'per_2': per_2,
        'per_1': per_1,

    }




    context = {
       
       'product': product,
       'categories': cat,
       'images': image,
       'colors': clrs,
       'sizes': sz,
       'related_products': Rproducts,
       'ratings': rating,
       'ratings_data': ratings_data,
   }
    
    return render(req,'shop/product.html',context)





 

def get_session_id(req):
    session_id = req.session.session_key
    if not session_id:
        req.session.create()
        session_id = req.session.session_key
    return session_id


def addToCart(req):

    if req.method == "POST":
       
       product_pk = req.POST.get('product_pk')
       color_pk = req.POST.get('color_pk')
       size_pk = req.POST.get('size_pk')
       quantity = req.POST.get('quantity')


       
       product = products.objects.get(pk=product_pk)
       color = colors.objects.get(pk=color_pk)
       size = sizes.objects.get(pk=size_pk)

       if req.user.is_authenticated:
             user = req.user

             existing_cart,created_cart = cart.objects.get_or_create(user=user)

             if existing_cart:
                 pcart = existing_cart
             else: 
                pcart = created_cart
                

             existing_item,created_item = cartItem.objects.get_or_create(cart=pcart,product=product,color=color,size=size)



             if not created_item:
                 
                 if existing_item.quantity == None:
                     existing_item.quantity = 0
                 

                 existing_item.quantity = int(existing_item.quantity) + int(quantity)

                 existing_item.save()

             else:
             
               existing_item.quantity = quantity
               existing_item.save()

       else:
           session_id = get_session_id(req)

           existing_cart,created_cart = cart.objects.get_or_create(session_id=session_id)

           if existing_cart:
                 pcart = existing_cart
           else: 
                pcart = existing_cart
                

           existing_item,created_item = cartItem.objects.get_or_create(cart=pcart,product=product,color=color,size=size)

           if not created_item:
                 existing_item.quantity = int(existing_item.quantity) + int(quantity)

                 existing_item.save()
           else:
               existing_item.quantity = quantity
               existing_item.save()
        
       return redirect('shop:productDetail',slug=product.slug)
    

    

def view_cart(req):

    

    user = req.user

    if not user.is_authenticated:

        session_id = get_session_id(req)

        try:

          user_cart = cart.objects.get(session_id=session_id)

        except cart.DoesNotExist:
            user_cart = None


    else:

         user_cart = cart.objects.get(user=user)


    cart_items = cartItem.objects.filter(cart=user_cart)

    
   

    discount = 0



    


    # products_total = sum(item.get_total() for item in cart_items)

    num = cart_items.count()

    products_total = 0

    for item in cart_items:
         products_total = products_total + item.get_total()  

    code = ''  
    order_coupon = None


    if req.method == "POST":
        code = req.POST.get('code')

        try:

          order_coupon = coupons.objects.get(code=code)

        except coupons.DoesNotExist:

            order_coupon = None
            discount = 0

        if order_coupon:

          if order_coupon.is_valid():

            if order_coupon.discount_type == 'percentage':
                discount = (order_coupon.discount_value*products_total)/100

            else:
                discount = order_coupon.discount_value



    tax = 0  # for this type tax is always 0 becuase it is included in product price
    delivery = 99 # if you want make it get from database

    total = products_total + tax + delivery - discount

    context = {

        'items': cart_items,
        'products_total': products_total,
        'tax': tax,
        'delivery': delivery,
        'total': total,
        
        'discount': discount,
        'code': order_coupon,
    }

    return render(req,'shop/cart.html',context)



def checkout(req):

    

    user = req.user

    if not user.is_authenticated:

        return redirect('users:login')

     
     
    user_cart = cart.objects.get(user=user)


    cart_items = cartItem.objects.filter(cart=user_cart)

    
    existing,created = addressf.objects.get_or_create(user=user)

    if not created:
        address = existing
    else:
        address = existing

    discount = 0



    


    # products_total = sum(item.get_total() for item in cart_items)

    num = cart_items.count()

    products_total = 0

    for item in cart_items:
         products_total = products_total + item.get_total()  

    code = ''  
    order_coupon = None


    if req.method == "POST":
        code = req.POST.get('code')

        print(code)

        try:

          order_coupon = coupons.objects.get(code=code)

        except coupons.DoesNotExist:

            order_coupon = None
            discount = 0

        if order_coupon:

          if order_coupon.is_valid():

            if order_coupon.discount_type == 'percentage':
                discount = (order_coupon.discount_value*products_total)/100

            else:
                discount = order_coupon.discount_value

        



    tax = 0  # for this type tax is always 0 becuase it is included in product price
    delivery = 99 # if you want make it get from database

    total = products_total + tax + delivery - discount

    context = {

        'items': cart_items,
        'products_total': products_total,
        'tax': tax,
        'delivery': delivery,
        'total': total,
        'addressf': address,
        'discount': discount,
        'code': order_coupon,
    }

    return render(req,'shop/checkout.html',context)



def removeFromCart(req,item_id):
    
    item = cartItem.objects.get(pk=item_id)
    item.delete()
    return redirect('shop:view_cart')

def quantity_inc(req,item_id):

    item = cartItem.objects.get(pk=item_id)
    item.quantity += 1
    item.save()
    return redirect('shop:view_cart')

def quantity_desc(req,item_id):

    item = cartItem.objects.get(pk=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    
    return redirect('shop:view_cart')

