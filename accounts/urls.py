# accounts/urls.py
from django.urls import path, include

from . import views

app_name= 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('myaccount/', views.myaccount, name='myaccount'),
]