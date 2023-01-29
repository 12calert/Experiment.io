from django.shortcuts import render

def homepage(request):
    context = {}
    return render(request, 'home.html', context=context)