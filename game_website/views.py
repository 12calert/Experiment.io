from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition

import secrets
from .forms import GameConditions, ChooseGame

def homepage(request):
    # create a session id for anonymous users and add
    request.session['user_id'] = secrets.token_hex(8)
    context={}
    chooseGame = ChooseGame(request.POST or None)
    context['chooseGame'] = chooseGame
    if request.POST:
        if chooseGame.is_valid():
            #send to appropriate game rooms page
            return redirect("all_rooms", game = chooseGame.cleaned_data.get("game_choice"))
    return render(request, 'home.html', context)

def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

def game_view(request, room_name):
    return render(request, 'game_view.html', {"room_name":room_name, "rect_img": "{% static 'images/logo.png' %}" }) # dict to store room number

def all_rooms(request, game):
    #rooms with one player waiting for another
    rooms = Game.objects.filter(users=1, game_type=game)
    # return response
    return render(request, 'all_rooms.html', {'rooms':rooms})

def create_room(request, game):
    # create the room
    #choose a condition to apply to the game
    conditions = Condition.objects.filter(game_type = game)
    # some way to pick which condition randomly, or with some logic here:
    condition = conditions.first()
    #note that this will fail if there is no condition
    if condition:
        # if the user selects a Public room:
        if 'Public' in request.POST:
            chat = Chat.objects.create()
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), 
            game_id = chat, public_yes_or_no=True,
            game_type=game, has_condition = condition)
            return redirect('game_view', room_name = new_room.room_name)
    # if the user selects a Private room:
        elif 'Private' in request.POST:
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), game_id = chat, public_yes_or_no=False, 
                                   game_type=game, has_condition = condition)
            return redirect('game_view', room_name = new_room.room_name)
    else:
        print("A condition is not specified")
        return redirect("")


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
   
def gamelogic(request):
    context = { "rect_img": "{% static 'images/logo.png' %}" }
    return render(request, 'gamelogic.html', context=context)

def conditions(request):
    #filter by the researcher's ID
    context = {}
    create = GameConditions(request.POST or None)
    context['create'] = create

    current_researcher = Researcher.objects.filter(user=request.user).first()
    context['conditions'] = Condition.objects.filter(created_by = current_researcher)

    if request.POST:
        if create.is_valid():
            Condition.objects.create(amount_item = create.cleaned_data.get("amount_of_items"),
                                    restriction = create.cleaned_data.get("restriction"),
                                    active = create.cleaned_data.get("active"),
                                    game_type = create.cleaned_data.get("game_type"),
                                    created_by = current_researcher)
            
    return render(request, 'conditions.html', context)
