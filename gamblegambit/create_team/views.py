from django.shortcuts import render,redirect
from django.http import HttpResponse
import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from home.models import Matches

# Create your views here.

import requests   #get json data from locally hosted spider 

import dateparser
from .models import Matches
from django.db.utils import IntegrityError
from django.utils import timezone
#method to get data from locally stored json file static way
# f = open("upcominglist.json",)
# match_list = json.load(f)

def str_to_datetime_convt(matchTime):
    return (dateparser.parse(matchTime,settings={'RETURN_AS_TIMEZONE_AWARE': True}))

def time_ob_adder(matches):
    for match in matches:
        time = match["time"]
        if time[-1] != 'Z':
            match["time"] = time + ':00Z'
        match_time = str_to_datetime_convt(match["time"])
        match["time_obj"] = match_time
        
match_list = []
#method to get json data from locally hosted spider
def local_spider_run():
    global match_list
    r_local = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm')
    match_list = (r_local.json())['items']

#Method To get data from API (CS:GO matches data)
def api_request_run():
    global match_list
    resp = []
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
                match_dict["team_a_id"] = match["opponents"][0]["opponent"]["id"]
                match_dict["team_b_id"] = match["opponents"][1]["opponent"]["id"]
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

def search_team_title(title):
    for match in match_list:
        # print(match["title"]) for debug purpose
        if match["title"] == title:
            return match
    else:
        return None
#uncomment after DB duplicate deletion is done
#this method saves the matches to DB excluding the duplciation (unqiue tofather: titie, time, game)
# def match_DB_adder(match_list):
#     for match in match_list:
#         try:
#             Matches.objects.create(
#             title = match["title"],
#             team_a = match["team_a"],
#             team_b = match["team_b"],
#             team_a_flag =match.get("team_a_flag") if match.get("team_a_flag") else "None",
#             team_b_flag =match.get("team_b_flag") if match.get("team_b_flag") else "None",
#             roster = match.get("roster") if match.get("roster") else "None",
#             game = match["game"],
#             competation = match["competation"],
#             # country = match.get("country")
#             time = match["time"],
#             time_obj = match["time_obj"],
#             isUpcoming = True,
#             isOngoiing = False,
#             isCompleted = False,
#             result = match.get("result") if match.get("result") else "None",
#             photos = match.get("photos") if match.get("photos") else "None"
#         )
#         except IntegrityError:
#             print(match["title"]+"  is already in the database")
        
#         except:
#             print(match["title"]+ " Unexpected error")

# def match_status_updater():
#     matches = Matches.objects.all().iterator()
#     for match in matches:
#         # time = dateparser.parse(match.time_obj.ctime(),settings={'RETURN_AS_TIMEZONE_AWARE': False})
#         con = match.time_obj.timestamp()-timezone.now().timestamp()
#         if con <= 0:
#             print(match.title + " is live")
#             match.isUpcoming = False
#             match.isOngoiing = True
#             match.save()

local_spider_run()  #run local server to get data (rainbow six siege data)
api_request_run()   #run api to get data (cs:go data)
time_ob_adder(match_list)   #run this method to add time_obj 
# match_list.sort(key=lambda r:r["time_obj"]) #this inline function sort the match list acorrding to time_obj(datetime)
# match_DB_adder(match_list)  #this method adds matches in DB Matches
# match_status_updater()

def csgo_roster_adder(match):
    team_a_photos = []
    team_b_photos = []
    roster_a = match["team_a_id"]
    roster_b = match["team_b_id"]
    payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
    url_1 = f'https://api.pandascore.co/csgo/teams?filter[id]={roster_a}'
    url_2 = f'https://api.pandascore.co/csgo/teams?filter[id]={roster_b}'
    r_1 = requests.get(url_1,headers = payload)
    r_2 = requests.get(url_2,headers = payload)
    resp_1 = r_1.json()
    resp_2 = r_2.json()

    for player in resp_1[0]["players"]:
        photo = player.get("image_url") if not match.get("image_url") else "None"
        team_a_photos.append({player["name"]:photo})
    for player in resp_2[0]["players"]:
        photo = player.get("image_url") if not match.get("image_url") else "None"
        team_b_photos.append({player["name"]:photo})
    match["team_a_photos"] = team_a_photos
    match["team_b_photos"] = team_b_photos

def rsix_roster_adder(match):
    team_a_photos = []
    team_b_photos = []
    for player in match["photos"]:
        if player in match["roster"][match["team_a"]]:
            team_a_photos.append({player:match["photos"][player]})
        else:
            team_b_photos.append({player:match["photos"][player]})

    match["team_a_photos"] = team_a_photos
    match["team_b_photos"] = team_b_photos

def sample(request):
    # data = Matches.objects.all().iterator()
    return HttpResponse("data")

@login_required(login_url='login')
def create_team(request, title):
    # print(title)  for debug purpose
    # print(request.user.is_authenticated)  checks user is authenicted or not

    match = search_team_title(title)
    if match != None:
        if match["game"] == "Rainbow Six Siege":
            rsix_roster_adder(match)
        else:
            csgo_roster_adder(match)

        # return render(request,"create-team-js.html",{"match":match})
        return render(request,"create-team.html",match)
    else:
        return HttpResponse("Match is not available")