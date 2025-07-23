from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth.views import (
    
      PasswordResetView,
      PasswordResetDoneView,
      PasswordResetConfirmView,
      PasswordResetCompleteView,
      PasswordChangeView,
      PasswordChangeDoneView

)
from django.urls import reverse_lazy

app_name = 'users'

urlpatterns = [

   path('',views.form),
   path('order/',views.edit_profile,name='orders'),
   path('form/',views.form,name='form'),
   path('signup/',views.signup_view,name='signup'),
   path('login/',views.login_view,name="login"),
   path('logout/',views.logout_view,name="logout"),
   path('stripe_webhook/',views.stripe_webhook,name='stripe_webhook'),
#    path('profile/<username>/',views.profile),
   path('profile/',views.profile,name='profile'),
   path('torder/',views.torder,name='torders'),
   path('orderPlace/',views.orderPlace,name="orderPlace"),
   path('success/',views.success_view,name='success'),
   path('otracking/<int:id>',views.order_tracking,name="otracking"),
   path('cancel/<int:id>',views.cancel_order,name="cancel_order"),
   path('replace/<int:id>',views.replace_order,name="replace_order"),
   path('return/<int:id>',views.return_order,name="return_order"),
   path('review/<int:id>',views.review,name="review"),
   path('reviewselect/<int:id>',views.review_select,name="review_select"),







   path('editProfile/',views.edit_profile,name='editprofile'),
   path('passwordReset/',PasswordResetView.as_view(
       template_name = 'users/passwordReset.html',
       email_template_name = 'users/passwordResetEmail.html',
       subject_template_name = 'users/passwordResetSubject.txt',
       success_url = reverse_lazy('users:passwordResetDone'),
       from_email = 'varshithkuravti@gmail.com'
   ),name='passwordReset'),

   path('passwordReset/done/',PasswordResetDoneView.as_view(
       template_name = 'users/passwordResetDone.html'),name='passwordResetDone'),

   
   path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(
       template_name = 'users/passwordResetConfirm.html',
       success_url = reverse_lazy('users:passwordResetComplete')
   ),name='passwordResetConfirm'),
   
   
   path('reset/done/',PasswordResetCompleteView.as_view(
       template_name = 'users/passwordResetComplete.html'
   ),name='passwordResetComplete'),

   path('passwordChange/',PasswordChangeView.as_view(
       template_name = 'users/passwordChange.html',
       success_url = reverse_lazy('users:passwordChangeDone')
   ),name='passwordChange'),

   path('passwordChange/done/',PasswordChangeDoneView.as_view(
       template_name = 'users/passwordChangeDone.html'
   ),name = 'passwordChangeDone')
   


   
   
   
   ]
