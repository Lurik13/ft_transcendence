#from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    #return HttpResponse("Hello world! I'm Home.")
    return render(request, 'home.html')

def about(request):
    #return HttpResponse("My About page.")
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')

def game(request):
    return render(request, "pong.html")