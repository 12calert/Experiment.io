# accounts/urls.py
from django.urls import path, include

from . import views

app_name= 'accounts'

urlpatterns = [
    path('signup/', views.register, name='signup'),
    path('login/', views.register, name='login'),
    path('myaccount/', views.myaccount, name='myaccount'),
]