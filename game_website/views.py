from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher

from django.http import HttpResponse #why are these added?
from django.template import loader

from django.contrib import messages
from django.contrib.auth import authenticate, login
import secrets

def homepage(request):
    # create a session id for anonymous users and add
    request.session['user_id'] = secrets.token_hex(8)
    context={}
    return render(request, 'home.html', context=context)

def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

def game_view(request, room_name):
    return render(request, 'game_view.html', {"room_name":room_name}) # dict to store room number

def all_rooms(request):
    #rooms with one player waiting for another
    rooms = Game.objects.filter(users=1)
    # return response
    return render(request, 'all_rooms.html', {'rooms':rooms})

def create_room(request):
    # create the room
    chat = Chat.objects.create()
    new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), game_id = chat)
    return redirect('game_view', room_name = new_room.room_name)

def researcher_registration(request):
    context = {}
    return render(request, 'researcher_registration.html', context=context)

def researcher_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        password = request.POST['password']
        # just to test
        print(name, surname, email, password)
        Researcher.objects.create(name=name, email=email, surname=surname)
        return redirect("/home")
        
        
    context = { }
    return render(request, 'researcher_registration.html', context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        redirect("/home")
    else:
        # Return an 'invalid login' error message.
        messages.error(request,'Invalid username or password')