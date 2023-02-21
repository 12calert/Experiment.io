from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition

import secrets
from .forms import create_conditions

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
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        Researcher.objects.create(name=name, surname=surname, email = email, username = username, password=password)
        return redirect("/home")
        
        
    context = { }
    return render(request, 'researcher_registration.html', context)

def data(request):
    context = {}
    return render(request, 'data.html', context=context)

def conditions(request):
    #filter by the researcher's ID
    context = {}
    create = create_conditions(request.POST or None)
    context['create'] = create
    # currently is doing SELECT *, which is obviously bad
    # later will filter by researcher ID
    context['conditions'] = Condition.objects.all()
    if request.POST:
        if create.is_valid():
            Condition.objects.create(amount_item = create.cleaned_data.get("amount_items"),
                                    restriction = create.cleaned_data.get("restriction"))
            
    return render(request, 'conditions.html', context)