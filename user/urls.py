from django import views
from django.urls import path
from .views import HomePage, Logout, Register, Login, HomePage, About

urlpatterns = [
    #path('',HomePage,name='index' ),
    path('register',Register,name='register' ),
    path('homepage', HomePage, name='homepage' ),
    path('',Login,name='login' ),
    path('logout',Logout,name='logout' ),
    path('about',About,name='about' ),
]