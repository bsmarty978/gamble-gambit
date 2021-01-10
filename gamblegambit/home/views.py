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

import datetime as dt
import dateparser

def str_to_datetime_convt(match_time):
    if match_time[-1] != 'Z':
        match_time = match_time + 'Z'
    return dateparser.parse(match_time,settings={'TIMEZONE':'GMT+5:30','RETURN_AS_TIMEZONE_AWARE': False})

def time_ob_adder(matches):
    for match in matches:
        match_time = str_to_datetime_convt(match["time"])
        match["time_obj"] = match_time

#method to get data from locally stored json file static way
# f = open("upcominglist.json",)
# match_list = json.load(f)

#method to get json data from locally hosted spider
r_local = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm')
match_list = (r_local.json())['items']

#Method To get data from API
payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
r_api = requests.get("https://api.pandascore.co/csgo/matches/upcoming", headers = payload)
resp = r_api.json()
i = 0
limit = 10
for match in resp:
    if i<limit:
        try:
            match_dict = {}
            teama = match["opponents"][0]["opponent"]["name"]
            teamb = match["opponents"][1]["opponent"]["name"]

            match_dict["title"] = teama + " VS " + teamb 
            match_dict["team_a"] = teama
            match_dict["team_b"] = teamb
            match_dict["team_a_flag"] = match["opponents"][0]["opponent"]["image_url"]
            match_dict["team_b_flag"] = match["opponents"][1]["opponent"]["image_url"]
            match_dict["time"] = match["scheduled_at"]
            match_dict["game"] = match["videogame"]["name"]
            match_dict["competation"] = match["league"]["name"]

            match_list.append(match_dict)
            i = i+1
        except:
            i = i+1
            limit = limit + 1
    else:
        break

time_ob_adder(match_list)


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