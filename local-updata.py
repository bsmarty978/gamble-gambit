import requests
import json
import datetime as dt
import dateparser
import time
from dateutil import tz
#Method To get data from API
# payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
# r_api = requests.get("https://api.pandascore.co/csgo/matches/upcoming", headers = payload)
# r_api = requests.get("http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm")
# match_list = (r_api.json())['items']

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
now = dt.datetime.now()
local_now = now.astimezone()
local_tz = local_now.tzinfo
local_tzname = local_tz.tzname(local_now)
print(local_tzname)

ex="Sunday, January 10, 2021 15:30 GMT+5:30"
exrp = "2021-01-10T10:00"                       #UTC time    dt.datetime.utcnow() use this method to get utc current time
exp = "2021-01-10T08:00:00Z" 
                   #Local time  dt.datetime.now()    use this method to get local current time
def str_to_datetime_convt(match_time):
    if match_time[-1] != 'Z':
        match_time = match_time + 'Z'
    return dateparser.parse(match_time,settings={'TIMEZONE':'GMT+5:30','RETURN_AS_TIMEZONE_AWARE': False})

# new_time = dateparser.parse(exp,settings={'TIMEZONE':'GMT+5:30','RETURN_AS_TIMEZONE_AWARE': False})
# new_time = dateparser.parse("4 hours ago")
print(str_to_datetime_convt(exp).ctime())

print(dt.datetime.now().ctime())
print(dt.datetime.utcnow().ctime())
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