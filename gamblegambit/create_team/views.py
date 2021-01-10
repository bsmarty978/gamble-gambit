from django.shortcuts import render,redirect
from django.http import HttpResponse
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
# Create your views here.

import requests   #get json data from locally hosted spider 

#method to get data from locally stored json file static way
# f = open("upcominglist.json",)
# match_list = json.load(f)

#method to get json data from locally hosted spider
r = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm')
match_list = (r.json())['items']


def search_team_title(title):
    for match in match_list:
        # print(match["title"]) for debug purpose
        if match["title"] == title:
            return match
    else:
        return None

def sample(request):
    return HttpResponse("hello app is working")

@login_required(login_url='login')
def create_team(request, title):
    # print(title)  for debug purpose
    # print(request.user.is_authenticated)  checks user is authenicted or not

    match = search_team_title(title)
    if match != None:
        team_a_photos = []
        team_b_photos = []
        for player in match["photos"]:
            if player in match["roster"][match["team_a"]]:
                team_a_photos.append({player:match["photos"][player]})
            else:
                team_b_photos.append({player:match["photos"][player]})

        match["team_a_photos"] = team_a_photos
        match["team_b_photos"] = team_b_photos

        # return render(request,"create-team-js.html",{"match":match})
        return render(request,"create-team.html",match)
    else:
        return HttpResponse("Match is not available")