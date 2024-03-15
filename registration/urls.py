from django.urls import path
from . import views


urlpatterns = [
    path('newreg/',views.newregistration, name='registration'),
    path('otpveri/',views.otpverify, name='otpverify'),
    path('login/',views.userlogin, name='login'),
    path('profile/',views.userprofile, name='profile'),
    path('chpass/',views.userchangepass, name='chpass'),
    path('logout/',views.userlogout, name='logout'),
    path('forpass/',views.userforgotpass, name='forpass'),
    path('resetpass/',views.userresetpass, name='resetpass'),
    path('userdet/<int:pk>',views.userdetailpage, name='userdetails'),
]
