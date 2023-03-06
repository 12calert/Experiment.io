from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition, Player, Experiment

import secrets
from .forms import GameConditions, ChooseGame, ExperimentForm
from random import choice

ROLE_CHOICES = ["follower", "giver"]
def homepage(request):
    # create a session id for anonymous users and add
    request.session['user_id'] = secrets.token_hex(5)
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

def game_view(request, game, room_name):
    foundGame = Game.objects.get(room_name = room_name)
    
    # Using filter() and first() to allow the case in which someone chooses to play with themself
    # change this in production to get() instead and handle exceptions accordingly reject the connection and
    # inform the player that they must play with someone else

    # ------- READ ME ----------
    #WARNING: THIS WILL RESULT IN INCONSISTENT ROLE ALLOCATION WHEN PLAYING BY YOURSELF
    # FOR CONSISTENT ALLOCATION USE TWO DIFFERENT BROWSERS
    foundPlayer = Player.objects.filter(game = foundGame, user_session = request.session.get("user_id")).first()
    return render(request, 'game_view.html', {"room_name":room_name, "rect_img": "{% static 'images/logo.png' %}", 
                                              "game":game, "player":foundPlayer}) # dict to store room number

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
            #chat = Chat.objects.create()
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public_yes_or_no=True,
            game_type=game, has_condition = condition)
            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))

            return redirect('game_view',  game = game, room_name = new_room.room_name)
    # if the user selects a Private room:
        elif 'Private' in request.POST:
            #chat = Chat.objects.create()
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public_yes_or_no=False, 
                                   game_type=game, has_condition = condition)
            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))
            return redirect('game_view', game = game, room_name = new_room.room_name)
    else:
        print("A condition is not specified")
        # do stuff, let user know there was error
        return redirect("home")

def joinRoom(request, game):
    # check which role the user will be assigned then connect them to the room
    if request.method == 'POST':
        room_name = request.POST['room']
        foundGame = Game.objects.get(room_name = room_name)
        # find what role the player already assigned is
        assignedRole = Player.objects.get(game = foundGame).role
        new_roles = [v for v in ROLE_CHOICES if v != assignedRole]
        Player.objects.create(role = choice(new_roles), game = foundGame, user_session = request.session.get("user_id"))

        return redirect('game_view', game = game, room_name = foundGame.room_name)

def researcher_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        Researcher.objects.create(name=name, surname=surname, email = email, username = username, password=password)
        return redirect("home")
        
        
    context = { }
    return render(request, 'researcher_registration.html', context)

def data(request):
    context = {}
    current_researcher = Researcher.objects.get(user=request.user)
    context['conditions'] = Condition.objects.filter(created_by = current_researcher)
    context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
    context['games'] = Game.objects.all() # very bad change later only for prototype
    context['chats'] = Chat.objects.all() # very bad change later only for prototype
    return render(request, 'data.html', context)
   
def gamelogic(request):
    context = { "rect_img": "{% static 'images/logo.png' %}" }
    return render(request, 'gamelogic.html', context=context)

def conditions(request):
    #filter by the researcher's ID
    context = {}
    create_condition = GameConditions(request.POST or None)
    create_experiment = ExperimentForm(request.POST or None)
    context['create_experiment'] = create_experiment
    context['create_condition'] = create_condition


    current_researcher = Researcher.objects.get(user=request.user)
    context['conditions'] = Condition.objects.filter(created_by = current_researcher)
    context['experiments'] = Experiment.objects.filter(created_by = current_researcher)

    return render(request, 'conditions.html', context)

def createExperiment(request):
    create_experiment = ExperimentForm(request.POST or None)
    if request.POST and create_experiment.is_valid():
        #do stuff from the experiment form
        current_researcher = Researcher.objects.get(user=request.user)
        Experiment.objects.create(name = create_experiment.cleaned_data.get("experiment_name"),
                                created_by = current_researcher)
    return redirect('game_conditions')

def createCondition(request):
    create_condition = GameConditions(request.POST or None)
    if request.POST and create_condition.is_valid():
        current_researcher = Researcher.objects.get(user=request.user)
        Condition.objects.create(amount_item = create_condition.cleaned_data.get("amount_of_items"),
                                restriction = create_condition.cleaned_data.get("restriction"),
                                active = create_condition.cleaned_data.get("active"),
                                game_type = create_condition.cleaned_data.get("game_type"),
                                created_by = current_researcher,
                                name = create_condition.cleaned_data.get("condition_name"),
                                experiment = create_condition.cleaned_data.get("experiment"))
    return redirect('game_conditions')