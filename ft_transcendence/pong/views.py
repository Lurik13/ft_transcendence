from django.shortcuts import render
from django.views import generic
from django.shortcuts import render
from .models import Game


# Create your views here.

def game(request):
    return render(request, "pong/pong.html", {})

# class PongView(generic.DetailView):
#     template_name = "pong/pong.html"
#     model = Game