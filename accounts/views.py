# accounts/views.py
from django.shortcuts import render
from accounts.forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import Researcher
from django.shortcuts import redirect
from uuid import uuid4
from django.shortcuts import render
from datetime import datetime
from accounts.models import Researcher  
# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

def myaccount(request):
    context = {}
    return render(request, 'myaccount.html', context=context)
@csrf_exempt
@csrf_protect
def register(request):
	if request.method == "POST":
		form = Researcher(request.POST)
		if form.is_valid():
        	    # form.save()
			user = form.save()
   			
			user.set_password(request.POST['password'])
			user.save()
			our_user = CustomUser(name=form.cleaned_data['name'], surname=form.cleaned_data['surname'], user_id=uuid4(), username=user, email=form.cleaned_data['email'])
			our_user.save()
			login(request, user)
   			# form.save()
			messages.success(request, "Registration successful." )
			return redirect("/home")
			
		messages.error(request, "Unsuccessful registration. Invalid information.")
  
	form = RegisterForm()
	return render (request=request, template_name="registration/signup.html", context={"register_form":form})


def my_form(request):
  if request.method == "POST":
    form = Researcher(request.POST)
    if form.is_valid():
      form.save()
  else:
      form = Researcher()
  return render(request, 'cv-form.html', {'form': form})

# def register(request):
#   if (request.method == 'POST'):
#     name = request.POST.get('name')
#     email = request.POST.get('email')
#     surname = request.POST.get('surname')
#     password=request.POST.get('password')
#     Researcher.save()
#   return render(request, 'researcher_login.html')