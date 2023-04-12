from django.shortcuts import render, redirect
from accounts.models import Game, Chat, Researcher, Condition, Player, Experiment, Move
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import secrets
from .forms import GameConditions, ChooseGame, ExperimentForm, ResearcherRegisterForm
from random import choice, randint
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib import messages
from math import floor
import json
from django.urls import reverse
# custom shapes module allows us to easily change values (also to apply custom conditions)
from game_website.shapes import randomColour, randomShape
import game_website.serialize as customSerializers

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
            game_type = chooseGame.cleaned_data.get("game_choice")
            if game_type == "MT":
                return redirect("map_task", game = game_type)
            # this where the other game type redirects would go
            else:
                return render(request, 'home.html', context)
            
    return render(request, 'home.html', context)

def mapTask(request, game):
    context={}
    # create the ChooseGame form
    chooseGame = ChooseGame(request.POST or None)
    if request.POST:  # if form submission
        #send to appropriate rooms page
        return redirect("all_rooms", game = game)
    return render(request, 'map_task.html', context)

""" view to render the login page, currently unused"""
def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

""" view to render the terms and conditions page """
def terms_and_conditions(request):
    context = {}
    return render(request, 'terms_and_conditions.html', context=context)

""" login page error message wrong credentials handling """
class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.set_level(self.request, messages.ERROR)
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)
    
""" renders the game view page which users play the game and chat to each other in"""
def game_view(request, game, room_name):
    # query the database to find the correct game instance
    foundGame = Game.objects.get(room_name = room_name, game_type = game)
    # Using filter() and first() to allow the case in which someone chooses to play with themself
    # change this in production to get() instead and handle exceptions accordingly reject the connection and
    # inform the player that they must play with someone else

    # ------- READ ME ----------
    #WARNING: THIS WILL RESULT IN INCONSISTENT ROLE ALLOCATION WHEN PLAYING BY YOURSELF
    # FOR CONSISTENT ALLOCATION USE TWO DIFFERENT BROWSERS

    # IMPORTANT: second parameter defines the default value if there is no found cookie, we use the width of 
    # 1366px since that is the most commonly used screenwidth, this may cause some undefined behaviour though
    conatinerSize = (request.session.get("width", 1366)/12*8)
    try:
        foundPlayer = Player.objects.get(game = foundGame, user_session = request.session.get("user_id"))
    # if the player has not got a cookie set one and add them to the DB
    except Player.DoesNotExist:
        tempSession = secrets.token_hex(5)
        foundPlayer = Player.objects.create(game = foundGame, user_session = tempSession)
        request.session['user_id'] = secrets.token_hex(5)

    foundGame.refresh_from_db()
    return render(request, 'game_view.html', {"room_name":room_name, "rect_img": "{% static 'images/logo.png' %}", 
                                              "game":game, "player":foundPlayer, "public":foundGame.public, "gameCurr":foundGame, 
                                              "containerSize":conatinerSize}) # dict to store room number

""" renders the page to see both maps"""
def seeMaps(request, game, room_name):
    foundGame = Game.objects.get(room_name = room_name)
    foundGame.refresh_from_db()
    containerSize = (request.session.get("width", 1366)/12*8)
    moves = serializers.serialize("json", Move.objects.filter(game=foundGame))
    return render(request, 'compare_maps.html', {"followerURL":foundGame.finishedFollowerURL, "giverURL":foundGame.finishedGiverURL,
                                                  "containerSize":containerSize, "moves":moves})

""" view which renders the page containing the list of rooms"""
def all_rooms(request, game):
    #query all rooms with one player waiting for another
    rooms = Game.objects.filter(users=1, game_type=game)
    # return response
    return render(request, 'all_rooms.html', {'rooms':rooms})

""" TESTED checks if two objects are intersecting"""
def intersect(r1, r2):
    if (r1["left"] < r2["left"] + r2["width"] and r1["left"] + r1["width"] > r2["left"] and
        r1["top"] < r2["top"] + r2["height"] and r1["top"] + r1["height"] > r2["top"]):
        return True
    else:
        return False

""" TESTED checks if an object is out of bounds within some container"""
def outOfBounds(obj, containerWidth):
    if (obj["left"] < 0):
        return True
    elif (obj["left"]+obj["width"] > containerWidth):
        return True
    elif (obj["top"] < 0): # replace with top of container
        return True
    elif (obj["top"]+obj["height"] > 550): # replace with bottom of container
        return True
    else:
        return False
""" TESTED checks to see if the object is placeable in some container given a list of obstacles"""
def place(obj, obstacles, containerWidth):
    for obstacle in obstacles:
        if intersect(obj,obstacle):
            return False
    if outOfBounds(obj, containerWidth):
        return False
    else:
        return True

""" creates a private room"""
def create_room(request, game):

    # choose a random condition, can be extended to choose a condition fairly
    # (choose the condition with the least amount of games, etc...)

    #first filter all the conditions we can use for our game
    conditions = Condition.objects.filter(game_type = game)
    # pick a random condition
    condition = choice(list(conditions))
    #note that this will fail if there is no condition
    if condition:
    # if the user selects a Private room:
        if 'Private' in request.POST:
            # create the Game instance as private
            new_room = Game.objects.create(users = 0, room_name = secrets.token_hex(5), public=False, 
                                   game_type=game, has_condition = condition)
            # create the player instance and add it to the newly created game instance
            # amount of items to generate
            itemNo = condition.amount_item
            rects = []
            containerWidth = floor(request.session.get("width", 1366)/12*8)
            rects.append({"top": (randint(0,450)), #hardcoded values bad
                        "left": (randint(0,(containerWidth-100))),
                        "width": randint(50,100), # change as needed or take from condition (depending on how much control we give researcher)
                        "height": randint(50,100),
                        "shape": randomShape(),
                        "colour": randomColour()})
            if rects[0]["shape"] == "square":
                rects[0]["height"] = rects[0]["width"]
            failCounter = 0
            # width of the container to stop objects from overflowing
            placed = False
            failed = False
            # for each object to place on map
            for i in range(0, itemNo-1):
                placed = False
                while(not placed or failCounter > 1000):
                    tempRect = {"top": (randint(0,450)), #hardcoded values bad
                        "left": (randint(0,(containerWidth-100))),
                        "width": randint(50,100),
                        "height": randint(50,100),
                        "shape": randomShape(),
                        "colour": randomColour()}
                    if tempRect["shape"] == "square":
                        tempRect["height"] = tempRect["width"]
                # check if it intersects with any already added
                    for j in range(0, len(rects)):
                        if intersect(tempRect, rects[j]):
                            failCounter += 1
                            # if too many failures, then stop
                            failed = True
                            break
                    if (not failed):
                        rects.append(tempRect)
                        placed = True
                    else:
                        failed = False
            # the finished path
            path = []
            # initial placement
            path.append({"top":0,
                    "left": 0,
                    "width": 32,
                    "height":32})
            # the last step which was taken
            lastStep = path[0]
            # the directions which the path can take
            directions = ["right", "left", "up", "down"]
            # the direction to take on the next move
            direction = "right"
            # how many succesful steps has there been
            successfulSteps = 0
            for k in range(0, 150): # change these values to make path longer/shorter
                if successfulSteps % 15 == 0: # change modulo to make path more/less sporadic (change direction more/less)
                    # pick a new direction
                    new_direction = [v for v in directions if v != direction]
                    direction = choice(new_direction)
                if direction == "right":
                    # temporarily create the step 
                    tempStep = ({"top":lastStep["top"],
                                "left":lastStep["left"]+lastStep["width"],
                                "width": 32,
                                "height": 32})
                    # check if its able to be added to the map
                    if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                        path.append(tempStep)
                        lastStep = tempStep
                        successfulSteps += 1
                    else:
                        # pick a new direction
                        new_direction = [v for v in directions if v != direction]
                        direction = choice(new_direction)
                        continue
                elif direction == "left":
                    tempStep = ({"top":lastStep["top"],
                                "left":lastStep["left"]-lastStep["width"],
                                "width": 32,
                                "height": 32})
                    if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                        path.append(tempStep)
                        lastStep = tempStep
                        successfulSteps += 1
                    else:
                        new_direction = [v for v in directions if v != direction]
                        direction = choice(new_direction)
                        continue
                elif direction == "down":
                    tempStep = ({"top":lastStep["top"]-lastStep["height"],
                                "left":lastStep["left"],
                                "width": 32,
                                "height": 32})
                    if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                        path.append(tempStep)
                        lastStep = tempStep
                        successfulSteps += 1
                    else:
                        new_direction = [v for v in directions if v != direction]
                        direction = choice(new_direction)
                        continue
                else:
                    tempStep = ({"top":lastStep["top"]+lastStep["height"],
                                "left":lastStep["left"],
                                "width": 32,
                                "height": 32})
                    if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                        path.append(tempStep)
                        lastStep = tempStep
                        successfulSteps += 1
                    else:
                        new_direction = [v for v in directions if v != direction]
                        direction = choice(new_direction)
                        continue
            new_room.path = json.dumps(path)

            new_room.rects = json.dumps(rects)
            new_room.save()

            Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id", secrets.token_hex(5)))
            return redirect('game_view', game = game, room_name = new_room.room_name)
    else:
        print("A condition is not specified")
        # do stuff, let user know there was error
        return redirect("home")

""" If there is an already created public room, join that one, otherwise create a new one (button functionality of all_rooms.html") """ 
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
                    Player.objects.create(role=choice(new_roles), game=room, user_session=request.session.get("user_id", secrets.token_hex(5)))
                

                    return redirect('game_view', game=game, room_name=room.room_name)

    # if no suitable rooms were found, create a new room
    return create_room2(request, game)

""" Create a public room """ 
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
        itemNo = condition.amount_item
        rects = []
        containerWidth = floor(request.session.get("width", 1366)/12*8)
        rects.append({"top": (randint(0,450)), #hardcoded values bad
                    "left": (randint(0,(containerWidth-100))),
                    "width": randint(50,100),
                    "height": randint(50,100),
                    "shape":randomShape(),
                    "colour": randomColour()})
        if rects[0]["shape"] == "square":
            rects[0]["height"] = rects[0]["width"]
        failCounter = 0
        # width of the container to stop objects from overflowing
        placed = False
        failed = False
        # for each object to place on map
        for i in range(0, itemNo-1):
            placed = False
            while(not placed or failCounter > 1000):
                tempRect = {"top": (randint(0,450)), # hardcoded values bad
                    "left": (randint(0,(containerWidth-100))),
                    "width": randint(50,100),
                    "height": randint(50,100),
                    "shape":randomShape(),
                    "colour": randomColour()}
                if tempRect["shape"] == "square":
                    tempRect["height"] = tempRect["width"]
            # check if it intersects with any already added
                for j in range(0, len(rects)):
                    if intersect(tempRect, rects[j]):
                        failCounter += 1
                        # if too many failures, then stop
                        failed = True
                        break
                if (not failed):
                    rects.append(tempRect)
                    placed = True
                else:
                    failed = False
        
        path = []
        # initial placement
        path.append({"top":0,
                "left": 0,
                "width": 25,
                "height":25})
        # the last step which was taken
        lastStep = path[0]
        # the directions which the path can take
        directions = ["right", "left", "up", "down"]
        # the direction to take on the next move
        direction = "right"
        # how many succesful steps has there been
        successfulSteps = 0
        for k in range(0, 150): # change these values to make path longer/shorter
            if successfulSteps % 15 == 0: # change modulo to make path more/less sporadic (change direction more/less)
                # pick a new direction
                new_direction = [v for v in directions if v != direction]
                direction = choice(new_direction)
            if direction == "right":
                # temporarily create the step 
                tempStep = ({"top":lastStep["top"],
                            "left":lastStep["left"]+lastStep["width"],
                            "width": 25,
                            "height": 25})
                # check if its able to be added to the map
                if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                    path.append(tempStep)
                    lastStep = tempStep
                    successfulSteps += 1
                else:
                    # pick a new direction
                    new_direction = [v for v in directions if v != direction]
                    direction = choice(new_direction)
                    continue
            elif direction == "left":
                tempStep = ({"top":lastStep["top"],
                            "left":lastStep["left"]-lastStep["width"],
                            "width": 25,
                            "height": 25})
                if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                    path.append(tempStep)
                    lastStep = tempStep
                    successfulSteps += 1
                else:
                    new_direction = [v for v in directions if v != direction]
                    direction = choice(new_direction)
                    continue
            elif direction == "down":
                tempStep = ({"top":lastStep["top"]-lastStep["height"],
                            "left":lastStep["left"],
                            "width": 25,
                            "height": 25})
                if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                    path.append(tempStep)
                    lastStep = tempStep
                    successfulSteps += 1
                else:
                    new_direction = [v for v in directions if v != direction]
                    direction = choice(new_direction)
                    continue
            else:
                tempStep = ({"top":lastStep["top"]+lastStep["height"],
                            "left":lastStep["left"],
                            "width": 25,
                            "height": 25})
                if(place(tempStep,rects, containerWidth) and (tempStep not in path)):
                    path.append(tempStep)
                    lastStep = tempStep
                    successfulSteps += 1
                else:
                    new_direction = [v for v in directions if v != direction]
                    direction = choice(new_direction)
                    continue
        new_room.path = json.dumps(path)
        new_room.rects = json.dumps(rects)
        new_room.save()
        
            # create the Player instance and add it to the newly created game instance
        Player.objects.create(role = choice(ROLE_CHOICES), game = new_room, user_session = request.session.get("user_id", secrets.token_hex(5)))

        return redirect('game_view',  game = game, room_name = new_room.room_name)

""" Function to join a private room, if it exists, otherwise create a new one.""" 
def join_private_room(request, game):
    if request.method == 'POST':
        unique_room_key = request.POST.get("unique_room_box")
        try:
            found_game = Game.objects.get(room_name=unique_room_key, public=False)
            # Check if the room already has two players
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
            Player.objects.create(role = choice(new_roles), game = found_game, user_session = request.session.get("user_id", secrets.token_hex(5)))

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
        # redirect to home page
        return redirect(reverse('home'))
    return render(request, 'researcher_registration.html', context)

""" HTML page that renders the two different maps after a game completes """ 
def compareMaps(request):
    # query the database to find the correct game instance
    if request.method == "POST" and is_ajax(request):
        room_name = request.POST["roomName"]
        # find the game that was played
        game = Game.objects.get(room_name=room_name)
        canvasURL = request.POST["canvasURL"]
        role = request.POST["role"]
        if role == "follower":
            game.finishedFollowerURL = canvasURL
        elif role == "giver":
            game.finishedGiverURL = canvasURL
        game.save()
        return JsonResponse({"gameType":game.game_type, "room_name":room_name}, status=200)
    else:
        HttpResponse("")

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
        experiment = Experiment.objects.filter(name = experiment, created_by = request.POST["current_researcher"])
        conditions = list(Condition.objects.filter(experiment = experiment.first()))
        # i.e. there exists some conditions for the experiment
        if conditions or experiment:
            # serialise the list to JSON so it can be showed in html
            serialisedConditions = serializers.serialize('json', conditions )
            experiment = list(experiment)
            serialisedExperiment = serializers.serialize('json', experiment )
            return JsonResponse({"exist": True, "conditions": serialisedConditions, "experiment": serialisedExperiment}, status=200)
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

""" TESTED called when researcher chooses to view the chat logs for a specified game"""
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


""" tested called when a user sends a message in the chat box. Saves the message along with the role to the database"""
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

""" Accept terms and conditions """ 
def acceptTOS(request):
    request.session['TOSaccept'] = True
    return JsonResponse({},status = 200)

# TESTED
""" This function handles AJAX POST requests to decrement the number of users in a game.""" 
def decrementUsers(request):
    if request.method == "POST" and is_ajax(request):
        room_name = request.POST["roomName"]
        game = Game.objects.get( room_name=room_name )
        game.users -= 1
        game.save()
        return JsonResponse({},status = 200)
# TESTED
""" This function handles AJAX POST requests to set the initial position of a player in a game.""" 
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

""" This function handles AJAX POST requests to store the screen size in the user's session. """ 
# TESTED
def setScreensize(request):
    if request.method == "POST" and is_ajax(request):
        width = int(request.POST["width"])
        height = int(request.POST["height"])
        request.session['width'] = width
        request.session['height'] = height
        return JsonResponse({},status = 200)
    return HttpResponse("")

# TESTED
""" This function handles AJAX POST requests to save a move in a game. """
def saveMove(request):
    if request.method == "POST" and is_ajax(request):
        room_name = request.POST["roomName"]
        game = Game.objects.get( room_name=room_name )
        type = request.POST["type"]
        if request.POST["x"]:
            x = int(request.POST["x"])
            y = int(request.POST["y"])
        if type == "mv":
            Move.objects.create(game=game,
                        move_type = type,
                        oldPos = {'x': game.follower_position[ "x" ], 'y': game.follower_position[ "y" ]},
                        newPos = {'x': game.follower_position[ "x" ] + x * 32, 'y': game.follower_position[ "y" ] + y * 32},
                        )
            return JsonResponse({},status = 200)
        elif type == "un":
            Move.objects.create(game=game,
                        move_type = type
                        )
            return JsonResponse({},status = 200)
        else:
            return HttpResponse("")
        
""" This function handles AJAX POST requests to download JSON data for a single experiment. """
def downloadJson(request):
    if request.method == "POST" and is_ajax(request):
        experiment_name = request.POST["experiment_name"]
        current_researcher = request.POST["current_researcher"]
        experiment = Experiment.objects.get(name = experiment_name, created_by = current_researcher)
        serializer = customSerializers.ExperimentSerializer(instance = experiment)
        return JsonResponse(serializer.data, status=200)
    
""" This function handles AJAX POST requests to download JSON data for all experiments by a researcher. """
def downloadAll(request):
    if request.method == "POST" and is_ajax(request):
        current_researcher = request.POST["current_researcher"]
        experiments = Experiment.objects.filter(created_by = current_researcher)
        serializer = customSerializers.ExperimentSerializer(instance = experiments, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)

# --- end of ajax views ---
