import requests
import json
import datetime as dt
import dateparser
from .models import Matches
#Method To get data from API
# payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
# r_api = requests.get("https://api.pandascore.co/csgo/matches/upcoming", headers = payload)

#method to get data from local server
r_api = requests.get("http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm")
match_list = (r_api.json())['items']

def str_to_datetime_convt(match_time):
    if match_time[-1] != 'Z':
        match_time = match_time + 'Z'
    return dateparser.parse(match_time,settings={'TIMEZONE':'GMT+5:30','RETURN_AS_TIMEZONE_AWARE': False})

def time_ob_adder(matches):
    for match in matches:
        match_time = str_to_datetime_convt(match["time"])
        match["time_obj"] = match_time

def teamPhotoadder(match):
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


for match in match_list:
    match_time_obj = str_to_datetime_convt(match["time"])
    match["time_obj"] = match_time_obj
    teamPhotoadder(match)

# for soting the list
match_list.sort(key=lambda r:r["time_obj"])
print(match_list[0])
Matches.objects.create(
    title = match_list[0]["title"],
    team_a = match_list[0]["team_a"],
    team_b = match_list[0]["team_b"],
    team_a_flag = match_list[0]["team_a_flag"],
    team_b_flag = match_list[0]["team_b_flag"],
    game = match_list[0]["game"],
    competation = match_list[0]["competation"],
    country = match_list[0]["country"],
    time = match_list[0]["time"],
    time_obj = match_list[0]["time_obj"],
    # roster = models.ForeignKey(Roster,on_delete=models.CASCADE)
    roster = match_list[0]["roster"],
    photos = match_list[0]["photos"],
    team_a_photos = match_list[0]["team_a_photos"],
    team_b_photos = match_list[0]["team_b_photos"],
    isUpcoming = True,
    isOngoiing = False,
    isCompleted = False,
    result = {"result": 0}
)
# i = 0
# outdata = []
# while (i<10):
#     match_dict = {}
#     teama = resp[i]["opponents"][0]["opponent"]["name"]
#     teamb = resp[i]["opponents"][1]["opponent"]["name"]

#     match_dict["title"] = teama + " VS " + teamb 
#     match_dict["team_a"] = teama
#     match_dict["team_b"] = teamb
#     match_dict["team_a_flag"] = resp[i]["opponents"][0]["opponent"]["image_url"]
#     match_dict["team_b_flag"] = resp[i]["opponents"][1]["opponent"]["image_url"]
#     match_dict["time"] = resp[i]["scheduled_at"]
#     match_dict["game"] = resp[i]["videogame"]["name"]
#     match_dict["competation"] = resp[i]["league"]["name"]

#     outdata.append(match_dict)
#     i = i+1
                

# new_time = dateparser.parse(exp,settings={'TIMEZONE':'GMT+5:30','RETURN_AS_TIMEZONE_AWARE': False})
# new_time = dateparser.parse("4 hours ago")
# print(str_to_datetime_convt(exp).ctime())

# print(dt.datetime.now().ctime())
# print(dt.datetime.utcnow().ctime())
# print(new_time-dt.datetime.now()) 



# from datetime import datetime
# from dateutil import tz

# # METHOD 1: Hardcode zones:
# from_zone = tz.gettz('UTC')
# to_zone = tz.gettz('America/New_York')

# # METHOD 2: Auto-detect zones:
# from_zone = tz.tzutc()
# to_zone = tz.tzlocal()

# # utc = datetime.utcnow()
# utc = datetime.strptime('2011-01-21 02:37:21', '%Y-%m-%d %H:%M:%S')

# # Tell the datetime object that it's in UTC time zone since 
# # datetime objects are 'naive' by default
# utc = utc.replace(tzinfo=from_zone)

# # Convert time zone
# central = utc.astimezone(to_zone)