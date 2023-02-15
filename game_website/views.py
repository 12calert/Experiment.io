from django.shortcuts import render, redirect
from django.core.serializers import serialize
import uuid
from accounts.models import Game, Chat
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
    return render(request, 'all_rooms.html', {'rooms':rooms})

def create_room(request):
    # create the room
    chat = Chat.objects.create()
    new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), game_id = chat)
    return redirect('game_view', room_name = new_room.room_name)