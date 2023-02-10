from django.shortcuts import render
from django.core.serializers import serialize
import json
from accounts.models import Room

def homepage(request):
    # read model as JSON
    rooms = Room.objects.all()
    serialized_data = serialize("json", rooms)
    serialized_data = json.loads(serialized_data)
    return render(request, 'home.html', {'rooms': serialized_data})

def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

def game_view(request, room_name):
    return render(request, 'game_view.html', {"room_name":room_name}) # dict to store room number