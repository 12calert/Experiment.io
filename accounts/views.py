# accounts/views.py
from django.shortcuts import render
from accounts.forms import RegisterForm
from django.contrib.auth import login
from django.contrib import messages
from accounts.models import Researcher
from django.shortcuts import redirect
from uuid import uuid4


def myaccount(request):
    context = {}
    return render(request, 'myaccount.html', context=context)

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save(zz)
			user.set_password(request.POST['password'])
			user.save()
			our_user = CustomUser(name=form.cleaned_data['name'], surname=form.cleaned_data['surname'], user_id=uuid4(), username=user, email=form.cleaned_data['email'])
			our_user.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RegisterForm()
	return render (request=request, template_name="registration/signup.html", context={"register_form":form})