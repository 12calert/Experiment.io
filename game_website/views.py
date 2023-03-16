from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition, Player, Experiment
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import secrets
from .forms import GameConditions, ChooseGame, ExperimentForm, ResearcherRegisterForm
from random import choice
from django.contrib.auth.models import User

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
                                              "game":game, "player":foundPlayer, "public":foundGame.public}) # dict to store room number
""" view which renders the page containing the list of rooms"""
def all_rooms(request, game):
    #query all rooms with one player waiting for another
    rooms = Game.objects.filter(users=1, game_type=game)
    # return response
    return render(request, 'all_rooms.html', {'rooms':rooms})

""" creates the room and sends the user to it, can be either a public or private room"""
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
            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id"))
            return redirect('game_view', game = game, room_name = new_room.room_name)
    else:
        print("A condition is not specified")
        # do stuff, let user know there was error
        return redirect("home")

""" function which adds the player to the room they selected"""
def joinRoom(request, game):
    # check which role the user will be assigned then connect them to the room
    if request.method == 'POST':
        # get the room name
        room_name = request.POST['room']
        # find the Game instance which they want to join
        foundGame = Game.objects.get(room_name = room_name)
        # count how many players there are in the game
        players = Player.objects.filter(game=foundGame)
        # if there are more than 2 users in the same game, then reload the page.
        if (players.count() >= 2):
            # rooms with one player waiting for another
            rooms = Game.objects.filter(users=1, game_type=game)
            # return response
            return redirect('all_rooms', game)
            
        # will have some undefined behaviour if no players exist
        # get the role of the current player
        if players:
            assignedRole = players.first().role
        else:
            assignedRole = None
        # choose the new roles to assign
        new_roles = [v for v in ROLE_CHOICES if v != assignedRole]
        # create the player instance with one of the roles chosen randomly
        Player.objects.create(role = choice(new_roles), game = foundGame, user_session = request.session.get("user_id"))

        return redirect('game_view', game = game, room_name = foundGame.room_name)

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

""" called after experiment form, adds the input to the database"""
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
        context['create_experiment'] = create_experiment
        context['create_condition'] = create_condition

        current_researcher = Researcher.objects.get(userkey=request.user)
        context['conditions'] = Condition.objects.filter(created_by = current_researcher)
        context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
        return render(request, "conditions.html", context)

def createCondition(request):
    create_condition = GameConditions(request.POST or None, request=request)
    if request.POST and create_condition.is_valid():
        current_researcher = Researcher.objects.get(userkey=request.user)
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
        # this is necessary to not check for validations on this form
        create_experiment = ExperimentForm(None, request = request)
        context['create_experiment'] = create_experiment
        context['create_condition'] = create_condition

        current_researcher = Researcher.objects.get(userkey=request.user)
        context['conditions'] = Condition.objects.filter(created_by = current_researcher)
        context['experiments'] = Experiment.objects.filter(created_by = current_researcher)
        return render(request, "conditions.html", context)

def researcher_registration(request):
    create_researcher_registration = ResearcherRegisterForm(request.POST or None)
    context = {}
    context["register"] = create_researcher_registration
    if request.POST and create_researcher_registration.is_valid():
        forename = request.POST['forename']
        surname = request.POST['surname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        # is_active set to false until we authenticate them
        user = User.objects.create_user(username = username, email = email, password = password, is_active = False, first_name = forename, last_name = surname)
        Researcher.objects.create(userkey = user)
    return render(request, 'researcher_registration.html', context)

# --- start of ajax views ---
def gameComplete(request):
    # request should be ajax and method should be POST.
    if request.method == "POST" and is_ajax(request):
        # get the room name from JSON
        room_name = request.POST["roomName"]
        game = Game.objects.get(room_name=room_name)
        game.completed = True
        game.save()
        return HttpResponse('')
    else:
        print("something went wrong")
        return HttpResponse('')

def viewConditions(request):
    if request.method == "POST" and is_ajax(request):
        # get the experiment and find all its conditions
        experiment = request.POST.get("experiment_name", None)
        if not experiment:
            print("something went wrong")
            return HttpResponse("")
        conditions = list(Condition.objects.filter(experiment = Experiment.objects.get(name = experiment, created_by = request.POST["current_researcher"])))
        # i.e. there exists some conditions for the experiment
        if conditions:
            serialisedConditions = serializers.serialize('json', conditions )
            return JsonResponse({"exist": True, "conditions": serialisedConditions}, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

def viewGames(request):
    if request.method == "POST" and is_ajax(request):
        condition = request.POST.get("condition_name", None)
        if not condition:
            print("something went wrong")
            return HttpResponse("")
        #kinda bad
        games = list(Game.objects.filter(has_condition = Condition.objects.get(name = condition, 
                                experiment = Experiment.objects.get(name = request.POST["experiment_name"], created_by = request.POST["current_researcher"]))))
        if games:
            serialisedGames = serializers.serialize('json', games )
            return JsonResponse({"exist": True, "games": serialisedGames }, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

def viewChats(request):
    if request.method == "POST" and is_ajax(request):
        room_name = request.POST.get("room_name", None)
        if not room_name:
            print("something went wrong")
            return HttpResponse("")
        chats = list(Chat.objects.filter(game = Game.objects.get(room_name = room_name)))
        if chats:
            serialisedChats = serializers.serialize('json', chats )
            return JsonResponse({"exist": True, "chats": serialisedChats }, status=200)
        else:
            return JsonResponse({"exist": False}, status = 200)
    return HttpResponse("")

# this can potentially be made async
def saveMessage(request):
    if request.method == "POST" and is_ajax(request):
        # get the variables from post data
        role = request.POST["role"]
        message = request.POST["message"]
        room_name = request.POST["room_name"]
        Chat.objects.create(role=role, game = Game.objects.get(room_name=room_name), content = message)
        return JsonResponse({},status = 200)
    return HttpResponse("")
# --- end of ajax views ---

def gamelogic(request):
    context = {}
    return render(request, 'gamelogic.html', context=context)
