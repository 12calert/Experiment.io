# accounts/views.py
import json
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.views.generic import FormView
from django.urls import reverse


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


def myaccount(request):
    context = {}
    return render(request, 'myaccount.html', context=context)
