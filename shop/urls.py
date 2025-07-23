from django.urls import path
from django.urls import include,path
from . import views


app_name = 'shop'

urlpatterns = [

    path('',views.index,name='index'),
    path('products/',views.pds,name='products'),
    path('categories/',views.cts,name='categories'),
    path('category/<slug:slug>',views.category,name='category'),
    path('search/<slug:slug>',views.search,name="search"),
    path('product/<slug:slug>',views.productDetail,name='productDetail'),
    path('cart/',views.view_cart,name="view_cart"),
    path('addcart/',views.addToCart,name="addToCart"),
    path('checkout/',views.checkout,name="checkout"),

    path('removefromcart/<int:item_id>',views.removeFromCart,name="removeFromCart"),
    path('quantityinc/<int:item_id>',views.quantity_inc,name="quantity_inc"),
    path('quantitydesc/<int:item_id>',views.quantity_desc,name="quantity_desc"),

    
  
    
]