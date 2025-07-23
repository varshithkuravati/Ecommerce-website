from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
import stripe.error
from . import forms
from django.contrib.auth import authenticate,login,logout
from .forms import createuser,loginform,EditProfile
from django.contrib import messages
from .models import User,Profile,orders,orderItem
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .forms import addressForm
from shop.models import cart,cartItem,coupons,couponUsages,products
from .models import addressf
# Create your views here.

import requests
from django.conf import settings
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from datetime import datetime,timedelta
from django.utils import timezone
from shop.models import ratings,ratingImg

from django.core.cache import cache



def form(req):
    form1 = forms.createuser()
    return render(req, "form.html", {"forms": form1})

def signup(req):
    if req.method == "POST":
        form = createuser(req.POST)
        if form.is_valid():
            print("form is valid")
    return HttpResponse("signup page")

def signup_view(req):
    if req.user.is_authenticated:
        return redirect('core:home')
        # return redirect('users:form')
    if req.method == "POST":
        form = createuser(req.POST)
        if form.is_valid():
            user1 = form.save()
            login(req,user1)
            messages.success(req,"Account created successfully")
            return redirect('core:home')
            # return redirect('users:form')
        # return HttpResponse("form is not valid")
        return render(req,'users/signup.html',{'form':form})
    
    form = createuser()
    return render(req,'users/signup.html',{'form':form}) 

def login_view(req):
    if req.user.is_authenticated:
        return redirect('shop:index')
        # return redirect('users:form')
    if req.method == "POST":
        form = loginform(req.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(email=email,password=password)
            if user:

                temp_key = req.session.session_key
                
                cache.set(f"old_session",temp_key,timeout=60*60*24)


               
                login(req,user)
               
                messages.success(req,"login successful")
                return redirect('shop:index')  
                # return redirect('users:form') 
            else:
                # messages.error(req,"email or passowrd is incorrect")
                form.add_error(None,'Invalid email or password')

        return render(req,'users/login.html',{'form':form})
    else:
        form = loginform()
        return render(req,'users/login.html',{'form':form})

def logout_view(req):
    logout(req)
    return redirect('shop:index')

def order(req):
    return render(req,'shop/orders.html')

def torder(req):
    return render(req,'shop/otracking.html')

@login_required

# def profile(req,username):
#     user  = get_object_or_404(User,username=username)
#     profile = get_object_or_404(profile,user=user)
#     return render(req,'users/profile.html',{'profile':profile,'user':user})

def profile(req):
    # user  = get_object_or_404(User,username=username)
    user = req.user
    profile = get_object_or_404(Profile,user=req.user)
    # print(profile)
    return render(req,'users/profile.html',{'profile':profile,'user':user})
    # return render(req,'users/profile.html')





@login_required

def edit_profile(req):

    user = req.user

    user_oders = orders.objects.prefetch_related('order_item').filter(user=user).order_by('-Odate')

    



    if req.method == "POST":
        form = EditProfile(req.user.username,req.POST,req.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            phonenum = form.cleaned_data['phonenum']

            user = User.objects.get(id = req.user.id)
            user.email = email
            user.save()
            profile = Profile.objects.get(user = user)
            profile.name = name
            profile.phonenum = phonenum
            profile.save()
            messages.success(req,"profile updated successfully")

            profile = Profile.objects.get(user = user)
            form = EditProfile(req.user.username)

            return redirect('shop:order')
        
        profile = Profile.objects.get(id = req.user.id)
        return render(req,'shop/orders.html',{'form':form,'profile':profile,'user_orders':user_oders})
    else:
        profile = Profile.objects.get(id = req.user.id)
        form = EditProfile(req.user.username)
        return render(req,'shop/orders.html',{'form':form,'profile':profile,'user_orders':user_oders})
    

@csrf_exempt
def orderPlace(req):

    user = req.user



    if req.method == "POST":

        form = addressForm(req.POST)

        name = req.POST.get('name')
        address_form = req.POST.get('address')
        houseNo = req.POST.get('houseNo')
        city = req.POST.get('city')
        country = req.POST.get('country')
        state = req.POST.get('state')
        pincode = req.POST.get('pincode')
        phonenum = req.POST.get('phonenum')





        if form.is_valid():

            order_id = str(uuid.uuid4())

            # address = form.save(commit=False)
            # address.user = user
            # address.save()

            discount = 0

            address = addressf.objects.get(user=user)

            address.name = req.POST.get('name')
            address.address = req.POST.get('address')
            address.houseNo = req.POST.get('houseNo')
            address.city = req.POST.get('city')
            address.country = req.POST.get('country')
            address.state = req.POST.get('state')
            address.pincode = req.POST.get('pincode')
            address.phonenum = req.POST.get('phonenum')
            discount = req.POST.get('discount')
            code = req.POST.get('code')

            address.save()

            
            



            user_cart = cart.objects.get(user=user)
            cart_items = cartItem.objects.filter(cart=user_cart)

            product_total = sum(item.get_total() for item in cart_items)

            delivery = 99
            tax = 0

            total = product_total + delivery + tax - int(discount)

            est_date = datetime.now().date() + timedelta(days=7)
            today_date = datetime.now().date()
            proccessed_date = today_date + timedelta(days=1)
            shipped_date = today_date + timedelta(days=1)
            

            dates = {'ordered_date':today_date.strftime('%b %d, %Y'),'proccessed_date':proccessed_date.strftime('%b %d, %Y'),'shipped_date':shipped_date.strftime('%b %d, %Y'),'delivery_date':est_date.strftime('%b %d, %Y'),'cancel_date':'','return_date':'','replace':''}




            final_address = f"<p> {address.name} </p> <br> <p> {address.phonenum} </p> <br> <p> {address.houseNo} </p> <br> <p> {address.address} </p> <br> <p> {address.city} - {address.pincode} </p> <br> <p> {address.state}, {address.country} </p>"

            ordered = orders.objects.create(
                order_id = order_id,
                user = user,
                total = total,
                address = final_address,
                status = "payment pending",
                est_dates = dates,
                
            )

            for item in cart_items:

                order_item = orderItem.objects.create(

                    product = item.product,
                    order = ordered,
                    quantity = item.quantity,
                    price = item.product.price,
                    color = item.color,
                    size = item.size,


                )

            date = timezone.now()



            if not int(discount) == 0:

              coupon_use = couponUsages.objects.create(
                  coupon=code,
                  user=user,
                  used_at=date,
                  order=ordered,
                  discount=discount

                 )

            stripe_key = settings.STRIPE_SECRET_KEY

            headers = {

                    "Authorization": f"Bearer {stripe_key}",
                    "Content-Type": "application/x-www-form-urlencoded",
                }


            data = {

                    "success_url": "http://127.0.0.1:8000/users/success?session_id={CHECKOUT_SESSION_ID}",
                    "cancel_url": "http://127.0.0.1:8000/shop/cart/",
                    
                    "line_items[0][price_data][currency]": "usd",
                    "line_items[0][price_data][product_data][name]": order_id,
                    "line_items[0][price_data][unit_amount]": int(total*100),
                    "line_items[0][price_data][product_data][description]": "hello",
                    "line_items[0][quantity]": 1,



                    
                    "mode": "payment",
                    "payment_method_types[]": "card",
                }
            

            responce = requests.post(
                
                "https://api.stripe.com/v1/checkout/sessions",
                headers=headers,
                data=data,


                                )
            
            # print("Stripe response:", responce.status_code, responce.text)
            
            
            if responce.status_code == 200:
                    return JsonResponse({"url": responce.json()["url"]})
            else:
                 return JsonResponse({"error": responce.text}, status=400)


     

            # return redirect(session.url)
    

            # if payment is seccuss

    #     ordered.status = "processing"

    #     ordered.save()




    #     cart_items.delete()


    # return redirect('shop:index')



def success_view(req):

    session_id = req.GET.get("session_id")

    stripe_key = settings.STRIPE_SECRET_KEY

    headers = {

        "Authorization": f"Bearer {stripe_key}",

    }

    res = requests.get(

        f"https://api.stripe.com/v1/checkout/sessions/{session_id}",
        headers=headers,

    )

    checkout_data = res.json()
    payment_intent_id = checkout_data.get("payment_intent")


    list_items_res = requests.get(
        f"https://api.stripe.com/v1/checkout/sessions/{session_id}/line_items",
        headers=headers,

    )

    list_items = list_items_res.json()

    # print(list_items)

    product_name = list_items["data"][0]["description"]

    user_order = orders.objects.get(order_id=product_name)

    user_order.type = "order"

    user_order.status = "processing"

    user_order.payment_id = payment_intent_id

    user_order.save()

    user = req.user

    user_cart = cart.objects.get(user=user)
    cart_items = cartItem.objects.filter(cart=user_cart)

    cart_items.delete()

    context = {

        'order_id': user_order.order_id,
        'total': user_order.total,
        'date': user_order.Odate,

    }

    return render(req,'shop/success.html',context)






@csrf_exempt

def stripe_webhook(req):

    payload = json.loads(req.body)
   
    event = payload.get('type') 

    
    if event['type'] == 'checkout.session.completed':

        session = event['data']['object']


        payment_intent_id = session.get('payment_intent')

        session_id = session.get('id')

        headers ={
            "Authorization": "Bearer",
        }

        line_items_res = requests.get(
            f"https://api.stripe.com/v1/checkout/sessions/{session_id}/line_items",
            headers = headers,
        )

        if line_items_res.status_code == 200:
            list_items = line_items_res.json()["data"]

            order_id = list_items[0]['description']



        




        try:

            user_order = orders.objects.get(order_id=order_id)
            user_cart = cart.objects.get(user=user_order.user)
            
            cart_items = cartItem.objects.filter(cart=user_cart)

            user_order.status = "processing"

            user_order.payment_id = payment_intent_id

            user_order.save()

            cart_items.delete()

        except:

            user_order.status = 'payment failed'

            user_order.save()

    return HttpResponse(status=200)




# This will usefull to extend from payment to shipping when admmin pannel created


SHIPPO_API_URL = "https://api.goshippo.com"
SHIPP0_API_KEY = "your_shippo_api_key_here"  # Replace with your actual Shippo API key



def order_ship(req,id):

    shipment = {

        "address_from": {},
        "address_to": {},
        "parcel":[{
            "length": "10",
            "width": "10",
            "height": "10",
            "weight": "10",  # in grams
            "distance_unit": "cm",
            "mass_unit": "g",

        }]
    }

    headers = {

            "Authorization": "Bearer ",
            "Content-Type": "application/x-www-form-urlencoded",
        }
    
    res = requests.post(
        f"{SHIPPO_API_URL}/shipments",
        headers=headers,
        data=json.dumps(shipment)
    )

    rates = res.json()['data']

    selected_rate = rates[0]['object_id']  # Select the first rate for simplicity

    transaction = {
        "rate": selected_rate,
        "label_file_type": "PDF",
        
    }

    transaction_res = requests.post(
        f"{SHIPPO_API_URL}/transactions",
        headers=headers,
        data=json.dumps(transaction)
    )

    label_url = transaction_res.json().get('label_url')

    return redirect(label_url)







def order_tracking(req,id):

    user = req.user

    user_order = orders.objects.get(user=user,pk=id)

    order_items = orderItem.objects.filter(order=user_order)

  

    price = 0

    for item in order_items:
        price = int(item.get_total()) + price

    tax = 0

    delivery = 99
    
    try:
        coupon_used = couponUsages.objects.get(user=user,order=user_order)

        discount = coupon_used.discount

    except couponUsages.DoesNotExist:

        coupon_used = None
        discount = 0



   

    context = {

        'order_items': order_items,
        'user_order': user_order,
        'tax': tax,
        'delivery': delivery,
        'price': price,
        'discount': discount,
        
    }

    return render(req,'shop/otracking.html',context)


def review(req,id):

    user = req.user
    order_item = orderItem.objects.get(pk=id)
    if req.method == "POST":

        description = req.POST.get('content')
        value = req.POST.get('rating')
        images = req.FILES.getlist('images')

        

        existing,created = ratings.objects.get_or_create(user=user,product=order_item.product,orderitem=order_item)



        existing.value = value
        existing.description = description
        existing.save()

        if images:

              for image in images:
                rating_image = ratingImg.objects.create(
                    rating=existing,
                    image=image
                )
                rating_image.save()

        rate = ratings.objects.filter(product=order_item.product,orderitem=order_item)

        avg_value = 0

        for r in rate:

            avg_value += r.value

        rate_count = rate.count()

        avg_value = (avg_value/rate_count) if rate_count > 0 else 0

        product = products.objects.get(pk=order_item.product.pk)

        product.rating = avg_value

        product.save()

        
        return redirect('users:otracking',id=order_item.order.id)

    try:
        rating = ratings.objects.get(user=user,product=order_item.product,orderitem=order_item)
        
        rating_content = rating
    except ratings.DoesNotExist:

        rating_content = None


    context = {

        'order_item': order_item,
        'content': rating_content,
    }

    
    return render(req,'users/review.html',context)


def review_select(req,id):

    user = req.user

    order = orders.objects.get(user=user,pk=id)
    order_items = orderItem.objects.filter(order=order)

    context = {
        'order_items': order_items,
    }

    return render(req,'users/reviewSelect.html',context)





def cancel_order(req,id):

    user = req.user

    if req.method == "POST":
       
       reason = req.POST.get('reason')

       user_order = orders.objects.get(user=user,pk=id)

       user_order.type = "cancel"

       user_order.status = "processing"

       user_order.reason = reason

       user_order.est_dates['cancel_date'] = datetime.now().date().strftime('%b %d, %Y')
       user_order.est_dates['proccessed_date'] = datetime.now().date().strftime('%b %d, %Y')

       user_order.save()



    return redirect('users:otracking',id=id)
    

def replace_order(req,id):

    user = req.user

    if req.method == "POST":
         
         reason = req.POST.get('reason')

         user_order = orders.objects.get(user=user,pk=id)

         user_order.type = "replace"

         user_order.status = "processing"

         user_order.reason = reason

         user_order.est_dates['replace_date'] = (datetime.now().date() + timedelta(days=7)).strftime('%b %d, %Y')
         user_order.est_dates['shipped_date'] = (datetime.now().date() + timedelta(days=1)).strftime('%b %d, %Y')
         user_order.est_dates['proccessed_date'] = (datetime.now().date() + timedelta(days=1)).strftime('%b %d, %Y')

         user_order.save()

    return redirect('users:otracking',id=id)


def return_order(req,id):

    user = req.user

    if req.method == "POST":
       
       reason = req.POST.get('reason')

       user_order = orders.objects.get(user=user,pk=id)

       user_order.type = "return"

       user_order.status = "processing"

       user_order.reason = reason

       user_order.est_dates['return_date'] = (datetime.now().date() + timedelta(days=2)).strftime('%b %d, %Y')
       user_order.est_dates['proccessed_date'] = datetime.now().date().strftime('%b %d, %Y')

       user_order.save()

       return redirect('users:otracking',id=id)






    










    






       











    

            

