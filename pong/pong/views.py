from django.shortcuts import render, redirect

def homepage(request):
    return redirect('player/login/')

def about(request):
    return render(request, 'about.html')

def privacy_policy(request):
    return render(request, 'privacy-policy.html')




