from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition, Player, Experiment
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import secrets
from .forms import GameConditions, ChooseGame, ExperimentForm, ResearcherRegisterForm
from random import choice, random
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import Http404
import math
import json
from django.core.serializers.json import DjangoJSONEncoder

# helper methods
"""checks a request to see if it is an ajax request"""
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

ROLE_CHOICES = ["follower", "giver"]  # Array of roles, either follower or giver

""" view which renders the home page"""
def homepage(request):
    # create a session id for anonymous users and add to cookies
    request.session['user_id'] = secrets.token_hex(5)
    context={}
    # create the ChooseGame form
    chooseGame = ChooseGame(request.POST or None)
    context['chooseGame'] = chooseGame
    if request.POST:  # if form submission
        if chooseGame.is_valid():   # if the form is valid (no inputs are invalid)
            #send to appropriate game rooms page
            return redirect("all_rooms", game = chooseGame.cleaned_data.get("game_choice"))
    return render(request, 'home.html', context)

""" view to render the login page, currently unused"""
def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

# login page error message wrong credentials
class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.set_level(self.request, messages.ERROR)
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
""" renders the game view page which users play the game and chat to each other in"""
def game_view(request, game, room_name):
    # query the database to find the correct game instance
    foundGame = Game.objects.get(room_name = room_name)
    # Using filter() and first() to allow the case in which someone chooses to play with themself
    # change this in production to get() instead and handle exceptions accordingly reject the connection and
    # inform the player that they must play with someone else

    # ------- READ ME ----------
    #WARNING: THIS WILL RESULT IN INCONSISTENT ROLE ALLOCATION WHEN PLAYING BY YOURSELF
    # FOR CONSISTENT ALLOCATION USE TWO DIFFERENT BROWSERS

    # query the database to get the current logged in player
    foundPlayer = Player.objects.get(game = foundGame, user_session = request.session.get("user_id"))
    return render(request, 'game_view.html', {"room_name":room_name, "rect_img": "{% static 'images/logo.png' %}", 
                                              "game":game, "player":foundPlayer, "public":foundGame.public, "gameCurr":foundGame}) # dict to store room number
""" view which renders the page containing the list of rooms"""
def all_rooms(request, game):
    #query all rooms with one player waiting for another
    rooms = Game.objects.filter(users=1, game_type=game)
    # return response
    return render(request, 'all_rooms.html', {'rooms':rooms})

""" creates the room and sends the user to it, can be either a public or private room"""

def intersect(r1, r2):
    if (r1["left"] < r2["left"] + r2["width"] and r1["left"] + r1["width"] > r2["left"] and
        r1["top"] < r2["top"] + r2["height"] and r1["top"] + r1["height"] > r2["top"]):
        return True
    else:
        return False
def create_room(request, game):

    # choose a random condition, can be extended to choose a condition fairly
    # (choose the condition with the least amount of games, etc...)

    #first filter all the conditions we can use for our game
    conditions = Condition.objects.filter(game_type = game)
    # pick a random condition
    condition = choice(list(conditions))
    #note that this will fail if there is no condition
    if condition:
        # if the user selects a Public room:
        if 'Public' in request.POST:
            # create the Game instance as public
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public=True,
            game_type=game, has_condition = condition)
            # create the Player instance and add it to the newly created game instance
            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))

            return redirect('game_view',  game = game, room_name = new_room.room_name)
    # if the user selects a Private room:
        elif 'Private' in request.POST:
            # create the Game instance as private
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public=False, 
                                   game_type=game, has_condition = condition)
            # create the player instance and add it to the newly created game instance
            
            itemNo = condition.amount_item
            rects = []
            failCounter = 0
            for i in range(0, itemNo-1):
                rects.append({"top": math.floor(random() * 1000),
                    "left": math.floor(random() * 1000),
                    "width": 100,
                    "height": 100})
                for j in range(0, len(rects)-1):
                    if intersect(rects[j], rects[len(rects)-1]):
                        rects.pop(i)
                        i -= 1
                        failCounter += 1
                        if failCounter > 1000:
                            i = 1000
                            break
            new_room.rects = json.dumps(rects)
            new_room.save()

            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))
            return redirect('game_view', game = game, room_name = new_room.room_name)
    else:
        print("A condition is not specified")
        # do stuff, let user know there was error
        return redirect("home")

def join_or_create_room(request, game):
    # Get a list of available public rooms
    available_rooms = Game.objects.filter(public=True)

    for room in available_rooms:
        players_in_room = Player.objects.filter(game=room)

        if room.users < 2:
            player = Player.objects.filter(game=room, user_session=request.session.get("user_id")).first()

            if not player:
                # choose the new roles to assign
                assigned_roles = [p.role for p in players_in_room]
                new_roles = [v for v in ROLE_CHOICES if v not in assigned_roles]

                if new_roles:
                    # create the player instance with one of the roles chosen randomly
                    Player.objects.create(role=choice(new_roles), game=room, user_session=request.session.get("user_id"))
                

                    return redirect('game_view', game=game, room_name=room.room_name)

    # if no suitable rooms were found, create a new room
    return create_room2(request, game)


def create_room2(request, game,):
    #first filter all the conditions we can use for our game
    conditions = Condition.objects.filter(game_type = game)
    # pick a random condition
    condition = choice(list(conditions))
    #note that this will fail if there is no condition
    if condition:
        # if the user selects a Public room:
       
            # create the Game instance as public
        new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public=True,
        game_type=game, has_condition = condition)
        
            # create the Player instance and add it to the newly created game instance
        Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))

        return redirect('game_view',  game = game, room_name = new_room.room_name)

 

def join_private_room(request, game):
    if request.method == 'POST':
        unique_room_key = request.POST.get("unique_room_box")
        try:
            found_game = Game.objects.get(room_name=unique_room_key, public=False)
            # Check if the room already has two players
            players_in_room = Player.objects.filter(game=found_game)
            if found_game.users >= 2:
                
                messages.error(request, "The private room is already full.")
                return redirect('all_rooms', game)
            # Perform necessary operations to join the private room
            # will have unintended behaviour if a player joins a room which a player has joined, left, then joined again
            player = Player.objects.filter(game=found_game).first()
            # will have some undefined behaviour if no players exist, though they cannot join an empty room, only create
            # get the role of the current player
            if player:
                assignedRole = player.role
            else:
                assignedRole = None
            # choose the new roles to assign
            new_roles = [v for v in ROLE_CHOICES if v != assignedRole]
            # create the player instance with one of the roles chosen randomly
            Player.objects.create(role = choice(new_roles), game = found_game, user_session = request.session.get("user_id"))

            return redirect('game_view', game=game, room_name=found_game.room_name)  
        except Game.DoesNotExist:
            # Handle the case when the private room with the given key does not exist
            messages.error(request, "The private room key is invalid or does not exist.")
            return redirect('all_rooms', game)
    else:
        return redirect('all_rooms', game)
 


""" renders the data page"""
def data(request):
    context = {}
    # get the currently logged in researcher
    current_researcher = Researcher.objects.get(userkey=request.user)
    # pass the researcher and experiments objects to the html page
    context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
    context['researcher'] = current_researcher
    return render(request, 'data.html', context)

""" renders the conditions page"""
def conditions(request):
    #filter by the researcher's ID
    context = {}
    # initialise the create experiment and condition form
    create_condition = GameConditions(request.POST or None, request=request)
    create_experiment = ExperimentForm(request.POST or None, request=request)
    context['create_experiment'] = create_experiment
    context['create_condition'] = create_condition
    # get the reseacher and find their experiments and conditions and pass to html
    current_researcher = Researcher.objects.get(userkey=request.user)
    context['conditions'] = Condition.objects.filter(created_by = current_researcher)
    context['experiments'] = Experiment.objects.filter(created_by = current_researcher)

    return render(request, 'conditions.html', context)

""" called after experiment form complete, adds the input to the database"""
def createExperiment(request):
    # initialise the create experiment form
    create_experiment = ExperimentForm(request.POST or None, request=request)
    # if the form is valid
    if request.POST and create_experiment.is_valid():
        #get the current logged in researcher and add form data to database as new entry
        current_researcher = Researcher.objects.get(userkey=request.user)
        Experiment.objects.create(name = create_experiment.cleaned_data.get("experiment_name"),
                                active = create_experiment.cleaned_data.get("active"),
                                created_by = current_researcher)
        return redirect('game_conditions')
    # if the form is not valid
    else:
        context = {}
        # initialise the condition form as empty so we don't check validation
        create_condition = GameConditions(None, request = request)
        # pass forms to html
        context['create_experiment'] = create_experiment
        context['create_condition'] = create_condition

        current_researcher = Researcher.objects.get(userkey=request.user)
        context['conditions'] = Condition.objects.filter(created_by = current_researcher)
        context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
        return render(request, "conditions.html", context)

"""called after experiment form complete, adds the input to the database"""
def createCondition(request):
    # initialise game condition form
    create_condition = GameConditions(request.POST or None, request=request)
    #if the form input is valid
    if request.POST and create_condition.is_valid():
        #get the current logged in researcher
        current_researcher = Researcher.objects.get(userkey=request.user)
        # create the condition in the database
        Condition.objects.create(amount_item = create_condition.cleaned_data.get("amount_of_items"),
                                restriction = create_condition.cleaned_data.get("restriction"),
                                active = create_condition.cleaned_data.get("active"),
                                game_type = create_condition.cleaned_data.get("game_type"),
                                created_by = current_researcher,
                                name = create_condition.cleaned_data.get("condition_name"),
                                experiment = create_condition.cleaned_data.get("experiment"))
        return redirect('game_conditions')
    else:
        context = {}
        # do not check for validation on the experiment form & pass forms to html
        create_experiment = ExperimentForm(None, request = request)
        context['create_experiment'] = create_experiment
        context['create_condition'] = create_condition

        current_researcher = Researcher.objects.get(userkey=request.user)
        context['conditions'] = Condition.objects.filter(created_by = current_researcher)
        context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
        return render(request, "conditions.html", context)

""" renders page for researchers to register"""
def researcher_registration(request):
    # initialise registration form
    create_researcher_registration = ResearcherRegisterForm(request.POST or None)
    context = {}
    # pass form to html
    context["register"] = create_researcher_registration
    # if form inputs are valid
    if request.POST and create_researcher_registration.is_valid():
        forename = request.POST['first_name']
        surname = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password1']
        # create a django user (so they can log in)
        # is_active set to false until we authenticate them
        user = User.objects.create_user(username = username, email = email, password = password, is_active = False, first_name = forename, last_name = surname)
        # add researcher to db
        Researcher.objects.create(userkey = user)
    return render(request, 'researcher_registration.html', context)

# --- start of ajax views ---
""" called when the game is completed"""
def gameComplete(request):
    # request should be ajax and method should be POST.
    if request.method == "POST" and is_ajax(request):
        # get the room name from JSON
        room_name = request.POST["roomName"]
        # find the game that was played
        game = Game.objects.get(room_name=room_name)
        # set to completed and save in the database
        game.completed = True
        game.save()
        return HttpResponse('')
    # catch undefined behaviour
    else:
        print("something went wrong")
        return HttpResponse('')

""" called when researcher chooses to view conditions from an experiment"""
def viewConditions(request):
    # if valid request
    if request.method == "POST" and is_ajax(request):
        # get the experiment and find all its conditions
        experiment = request.POST.get("experiment_name", None)
        # catch undefined behaviour
        if not experiment:
            print("something went wrong")
            return HttpResponse("")
        # create a list of all the conditions for the experiment the researcher chooses to view
        conditions = list(Condition.objects.filter(experiment = Experiment.objects.get(name = experiment, created_by = request.POST["current_researcher"])))
        # i.e. there exists some conditions for the experiment
        if conditions:
            # serialise the list to JSON so it can be showed in html
            serialisedConditions = serializers.serialize('json', conditions )
            return JsonResponse({"exist": True, "conditions": serialisedConditions}, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

""" called when researcher chooses to view the games that have been played or are in progress which have some 
specified condition set on them"""
def viewGames(request):
    # if the request is valid
    if request.method == "POST" and is_ajax(request):
        # get the condition name from the page request
        condition = request.POST.get("condition_name", None)
        # catch undefined behaviour
        if not condition:
            print("something went wrong")
            return HttpResponse("")
        # create a list of games in which the specified condition was applied and it was the condition was created by the logged in user
        games = list(Game.objects.filter(has_condition = Condition.objects.get(name = condition, 
                                experiment = Experiment.objects.get(name = request.POST["experiment_name"], created_by = request.POST["current_researcher"]))))
        if games:
            # serialise list to JSON to view in html
            serialisedGames = serializers.serialize('json', games )
            return JsonResponse({"exist": True, "games": serialisedGames }, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

""" called when researcher chooses to view the chat logs for a specified game"""
def viewChats(request):
    # if request is valid
    if request.method == "POST" and is_ajax(request):
        # get the room name of the game from the page
        room_name = request.POST.get("room_name", None)
        # catch undefined behaviour
        if not room_name:
            print("something went wrong")
            return HttpResponse("")
        # get a list of chats in which for the specified game
        chats = list(Chat.objects.filter(game = Game.objects.get(room_name = room_name)))
        if chats:
            # serialise to JSON to view in html
            serialisedChats = serializers.serialize('json', chats )
            return JsonResponse({"exist": True, "chats": serialisedChats }, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

""" called when a user sends a message in the chat box. Saves the message along with the role to the database"""
def saveMessage(request):
    # if request is valid
    if request.method == "POST" and is_ajax(request):
        # get the variables from post data
        role = request.POST["role"]
        message = request.POST["message"]
        room_name = request.POST["room_name"]
        # add the chat into the database
        Chat.objects.create(role=role, game = Game.objects.get(room_name=room_name), content = message)
        return JsonResponse({},status = 200)
    return HttpResponse("")

def acceptTOS(request):
    request.session['TOSaccept'] = True
    return JsonResponse({},status = 200)

def initialPlayer(request):
    if request.method == "POST" and is_ajax(request):
        x = int(request.POST["x"])
        y = int(request.POST["y"])
        room_name = request.POST["room_name"]
        game = Game.objects.get( room_name=room_name )
        game.follower_position[ "x" ] = x
        game.follower_position[ "y" ] = y
        game.save()
        return JsonResponse({},status = 200)
    return HttpResponse("")
# --- end of ajax views ---
