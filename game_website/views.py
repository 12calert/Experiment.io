from django.shortcuts import render

def homepage(request):
    context = {}
    return render(request, 'home.html', context=context)

def researcher_login(request):
    context = {}
    return render(request, 'researcher_login.html', context=context)

def game_view(request):
    context = {}
    return render(request, 'game_view.html', context=context)