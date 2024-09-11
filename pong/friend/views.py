from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Friendship, Player
import logging


@login_required
def index(request):
    return render(request, "friend/index.html")

@login_required
def add(request):
    if request.method == 'POST':
        you = request.user
        you.last_login = timezone.now()
        you.save()
        if request.POST.get('username') == you.username:
            messages.add_message(request, messages.INFO, "can't add yourself")
            return render(request, "friend/add.html")
        users = Player.objects.filter(username=request.POST.get('username'))
        if len(users) == 0:
            messages.add_message(request, messages.INFO, ("user doesn't exist"))
            return render(request, "friend/add.html")
        new_friend = Friendship.objects.filter(Q(user=you, friend=users[0]) | Q(user=users[0], friend=you))
        if len(new_friend) != 0:
            messages.add_message(request, messages.INFO, ("invitation already sent"))
            return render(request, "friend/add.html")
        new_friend = Friendship(user=you, friend=users[0])
        new_friend.save()
        return render(request, "friend/work.html", {'friend':users[0], 'you':you})
        # Handle the submitted username as needed
        # For example, you can query the User model or process it in other ways
    return render(request, "friend/add.html")

@login_required    
def delete_friend(request, id_friendship):
    request = Friendship.objects.get(id=id_friendship)
    request.delete()
    return redirect("friend:list")

@login_required
def accept(request, id_friendship):
    request = Friendship.objects.get(id=id_friendship)
    request.status = 'accepted'
    request.save()
    return redirect("friend:pending")

@login_required
def refuse(request, id_friendship):
    request = Friendship.objects.get(id=id_friendship)
    request.status = 'refused'
    request.save()
    return redirect("friend:pending")

@login_required
def list(request):
    you = request.user
    friends = Friendship.objects.filter(Q(user=you, status='accepted') | Q(friend=you, status='accepted'))
    you.last_login = timezone.now()
    you.save()
    return render(request, "friend/list.html", {'friends':friends, 'you':you})

@login_required
def pending(request):
    you = request.user
    friends = Friendship.objects.filter(Q(friend=you, status='pending'))
    you.last_login = timezone.now()
    you.save()
    return render(request, "friend/pending.html", {'friends':friends, 'you':you})

@login_required
def refused(request):
    you = request.user
    friends = Friendship.objects.filter(Q(friend=you, status='refused'))
    you.last_login = timezone.now()
    you.save()
    return render(request, "friend/refused.html", {'friends':friends, 'you':you})