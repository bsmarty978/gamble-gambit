from django.db.models import base
from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# from home.models import Matches

# Create your views here.

import requests   #get json data from locally hosted spider 

import dateparser
from .models import Matches,MyTeam
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

# uncomment after DB duplicate deletion is done
# this method saves the matches to DB excluding the duplciation (unqiue tofather: titie, time, game)
def match_DB_adder(match_list):
    for match in match_list:
        try:
            Matches.objects.create(
            title = match["title"],
            team_a = match["team_a"],
            team_b = match["team_b"],
            team_a_flag =match.get("team_a_flag") if match.get("team_a_flag") else "https://siege.gg/img/player-silhouette-darker.svg",
            team_b_flag =match.get("team_b_flag") if match.get("team_b_flag") else "https://siege.gg/img/player-silhouette-darker.svg",
            roster = match.get("roster") if match.get("roster") else "None",
            game = match["game"],
            competation = match["competation"],
            # country = match.get("country")
            time = match["time"],
            time_obj = match["time_obj"],
            isUpcoming = True,
            isOngoiing = False,
            isCompleted = False,
            result = match.get("result") if match.get("result") else "None",
            photos = match.get("photos") if match.get("photos") else "None"
        )
        except IntegrityError:
            print(match["title"]+"  is already in the database")
        
        except:
            print(match["title"]+ " Unexpected error")

def match_status_updater():
    matches = Matches.objects.all().iterator()
    for match in matches:
        # time = dateparser.parse(match.time_obj.ctime(),settings={'RETURN_AS_TIMEZONE_AWARE': False})
        con = match.time_obj.timestamp()-timezone.now().timestamp()
        if con <= 0:
            print(match.title + " is live")
            match.isUpcoming = False
            match.isOngoiing = True
            match.save()

local_spider_run()  #run local server to get data (rainbow six siege data)
api_request_run()   #run api to get data (cs:go data)
time_ob_adder(match_list)   #run this method to add time_obj 
match_list.sort(key=lambda r:r["time_obj"]) #this inline function sort the match list acorrding to time_obj(datetime)
match_DB_adder(match_list)  #this method adds matches in DB Matches
match_status_updater()

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

    matchDB = Matches.objects.get(title= match["title"],time_obj=match["time_obj"])
    matchDB.team_a_photos = team_a_photos
    matchDB.team_b_photos = team_b_photos
    matchDB.save()

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

    matchDB = Matches.objects.get(title= match["title"],time_obj=match["time_obj"])
    matchDB.team_a_photos = team_a_photos
    matchDB.team_b_photos = team_b_photos
    matchDB.save()

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

@login_required(login_url='login')
def confirm_team(request, title):
    if request.method=="POST":
        my_cap = request.POST.get("my_cap")
        my_team = request.POST.getlist("my_roster[]")
        # stat = request.POST.get("state")
        match_title = request.POST.get("title")

        my_roster = {"my_cap":my_cap, "my_team":my_team}

        print(request.user.username)
        print(my_roster)
        # print(title)
        # print("================================")
        # try:
        try:
            myteam_obj = MyTeam.objects.get(match=Matches.objects.get(title=match_title),username=request.user.username)
        except:
            myteam_obj = None
        if myteam_obj:
            myteam_obj.user_captain = my_cap
            myteam_obj.user_roster = my_team
            myteam_obj.save()
            messages.success(request,request.user.username + " ,Your Team has been Set")


        else:
            MyTeam.objects.create(
                match = Matches.objects.get(title=match_title),
                username = request.user.username,
                user_captain = my_cap,
                user_roster = my_team
                
            )
            messages.success(request,request.user.username + " ,Your Team has been Set")


        # except IntegrityError:
        #     print("is already in the database")
        
        # except:
        #     print("Unexpected error")
     
        return HttpResponse("POST:your team is created" + str(my_roster))
        # return redirect("myteam", title)

    userTeam = MyTeam.objects.get(username=request.user.username,match=Matches.objects.get(title=title))
    basephotos = userTeam.match.team_a_photos
    basephotos.extend(userTeam.match.team_b_photos)
    user_team_photos = []
    for player in basephotos:
        name = list(player.keys())[0]
        if name in userTeam.user_roster:
            user_team_photos.append(player)
    print(user_team_photos)
    i = 0
    for player in user_team_photos:
        if list(player.keys())[0] == userTeam.user_captain:
            user_team_photos[i],user_team_photos[2] = user_team_photos[2],player
            break
        i += 1
    context = {
        "match": userTeam.match,
        "user_captain": userTeam.user_captain,
        "user_roster": userTeam.user_roster,
        "user_team_photos": user_team_photos
    }
    return render(request,"myTeam.html",context)


@login_required(login_url='login')
def upcoming(request):
    con =  match_list[0]["time_obj"].timestamp()-timezone.now().timestamp()
    if con <= 0:
        local_spider_run()  #run local server to get data (rainbow six siege data)
        api_request_run()   #run api to get data (cs:go data)
        time_ob_adder(match_list)   #run this method to add time_obj 
        match_list.sort(key=lambda r:r["time_obj"]) #this inline function sort the match list acorrding to time_obj(datetime)
        match_DB_adder(match_list)  #this method adds matches in DB Matches
        match_status_updater()

    return render(request,"upcoming.html", {'match_list':match_list})


def r6_match_result_spider():
    r_local = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=matches')
    return (r_local.json())['items']

@login_required(login_url='login')
def completedmatchList(request):
    # NOTE: method to add new completed matches to DB
    # r6_match_results = r6_match_result_spider()
    # time_ob_adder(r6_match_results)
    # for match in r6_match_results:
    #     title = match["title"]
    #     timem = match["time"]
    #     try:
    #         m = Matches.objects.get(title=match["title"],time = timem)
    #         m.score_a = float(match["result_a"])
    #         m.score_b = float(match["result_b"])
    #         m.save()
    #         print(m.title + "***********")
    #     except:
    #         Matches.objects.create(
    #         title = match["title"],
    #         team_a = match["team_a"],
    #         team_b = match["team_b"],
    #         team_a_flag =match.get("team_a_flag") if match.get("team_a_flag") else "https://siege.gg/img/player-silhouette-darker.svg",
    #         team_b_flag =match.get("team_b_flag") if match.get("team_b_flag") else "https://siege.gg/img/player-silhouette-darker.svg",
    #         roster = match.get("roster") if match.get("roster") else "None",
    #         game = match["game"],
    #         competation = match["competation"],
    #         # country = match.get("country")
    #         time = match["time"],
    #         time_obj = match["time_obj"],
    #         isUpcoming = False,
    #         isOngoiing = False,
    #         isCompleted = True,
    #         result = match.get("stats") if match.get("result") else "None",
    #         photos = match.get("photos") if match.get("photos") else "None",
    #         score_a = float(match["result_a"]),
    #         score_b = float(match["result_b"])
    #     )
    #         print(title + "###################")

    completed_list = []
    for match in Matches.objects.filter(isCompleted=True):
        print(match.title)
        data = {
            "title": match.title,
            "team_a": match.team_a,
            "team_b": match.team_b,
            "team_a_flag": match.team_a_flag,
            "team_b_flag": match.team_b_flag,
            "time": match.time,
            "time_obj": match.time_obj,
            "game": match.game,
            "competation": match.competation,
            "score_a" : match.score_a,
            "score_b" : match.score_b
        }
        completed_list.append(data)
    completed_list.sort(key=lambda r:r["time_obj"],reverse=True)
    return render(request,"results.html", {'match_list':completed_list})
