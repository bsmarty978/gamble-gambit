from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import CreateUserForm

import requests   #get json data from locally hosted spider 

#method to get data from locally stored json file static way
# f = open("upcominglist.json",)
# match_list = json.load(f)

#method to get json data from locally hosted spider
r = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm')
match_list = (r.json())['items']

@login_required(login_url='login')
def homePage(request):
    return render(request,"index.html")

def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request,username=username,password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username OR Password is incorrect")

        return render(request,"login.html")

def logoutUserPage(request):
    logout(request)
    return redirect("login")

def signupPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                user = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + user)
                return redirect("login")

        context ={"form":form}
        return render(request,"signup.html",context) 

@login_required(login_url='login')
def upcoming(request):
    return render(request,"upcoming.html", {'match_list':match_list})