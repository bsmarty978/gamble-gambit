from re import search
import requests
from requests import Session, Request
from proxy_requests import ProxyRequests
from bs4 import BeautifulSoup as btsp
from urllib.parse import quote,urlencode
# proxies = {
#  "http": "http://62.144.211.124:8080",
#  "https": "http://62.144.211.124:8080",
# }
# req = requests.get("https://www.google.com", proxies=proxies)
# https://api.pandascore.co/csgo/teams?filter[id]=125847,125847


# roster_a = 125847
# roster_b = 125847
# payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
# para = {"filter[id]": [roster_a,roster_b]}
# url = f'https://api.pandascore.co/csgo/teams'
# urll = url + urlencode(para)
# print(urll)
# r_api = requests.get(urll,headers = payload)
# resp = r_api.json()
# print(resp)
# urll = 'https://api.pandascore.co/csgo/teams?filter[id]=125847&filter[id]=125847'
# url = 'https://api.pandascore.co/csgo/teams'
# payload = {"Authorization" : "4p42JOzAXCi-3AqqTPfKs5ume17XCm9Kvmv6LTylSDFQxux6UHs"}
# request = Request('GET', urll, headers = payload)
# prepared = request.prepare()
# # prepared.url += '?filter[id]=125847%2C125847'
# session = Session()
# response = session.send(prepared)
# print(response.json())

# search_str = input("Search:")
# # search_str = "filmora 9"
# safe_search_str = quote(search_str, safe='')
# # print(safe_search_str)
# base_url = "https://www.1377x.to/"
# r = ProxyRequests(fr'{base_url}search/{safe_search_str}/1')

# r.get()
# html_doc = str(r)
# # print(r.get_status_code())  
# # print(html_doc)
# soup = btsp(html_doc, 'html.parser')
# result_list = soup.find_all('tr')

# data_list = []
# counter = 1
# for result in result_list:
#     try:
#         d = {}
#         id = counter
#         title = result.find_all('a')[1].get_text()
#         title_url = result.find_all('a')[1].get('href')
#         d["id"] = id
#         d["title"] = title
#         d["url"] = title_url
#         data_list.append(d)
#         counter = counter + 1
#     except:
#         pass
# # print(data_list)
# sub_r = ProxyRequests(fr'{base_url}{data_list[0]["url"]}')
# sub_r.get()
# sub_soup = btsp(str(sub_r),'lxml')
# magnet = sub_soup.find('a',{'class': 'l3426749b3b895e9356348e295596e5f2634c98d8'}).get('href')
# print(magnet)
import re
data = [
{"name": "Static", "rating": "0.86", "kd": "22-29 (-7)", "entry": "3-5 (-2)", "kost": "55%", "kpr": "0.50", "srv": "34%", "1vx": "1", "plant": "0", "hs": "52%"},
{"name": "h3dy", "rating": "0.85", "kd": "25-28 (-3)", "entry": "3-5 (-2)", "kost": "52%", "kpr": "0.57", "srv": "36%", "1vx": "0", "plant": "0", "hs": "55%"}, 
{"name": "EnvyTaylor", "rating": "1.14", "kd": "35-25 (+10)", "entry": "6-2 (+4)", "kost": "70%", "kpr": "0.80", "srv": "43%", "1vx": "1", "plant": "0", "hs": "63%"}, 
{"name": "Nova", "rating": "1.02", "kd": "22-24 (-2)", "entry": "4-4 (+0)", "kost": "68%", "kpr": "0.50", "srv": "45%", "1vx": "1", "plant": "6", "hs": "39%"}, 
{"name": "CATsang", "rating": "1.05", "kd": "37-31 (+6)", "entry": "6-7 (-1)", "kost": "57%", "kpr": "0.84", "srv": "30%", "1vx": "1", "plant": "0", "hs": "68%"},
{"name": "yass", "rating": "0.99", "kd": "29-29 (+0)", "entry": "2-4 (-2)", "kost": "68%", "kpr": "0.66", "srv": "34%", "1vx": "1", "plant": "0", "hs": "48%"}, 
{"name": "SyAIL", "rating": "0.98", "kd": "32-29 (+3)", "entry": "5-4 (+1)", "kost": "61%", "kpr": "0.73", "srv": "34%", "1vx": "0", "plant": "0", "hs": "55%"}, 
{"name": "JaekDow", "rating": "0.70", "kd": "16-34 (-18)", "entry": "4-6 (-2)", "kost": "57%", "kpr": "0.36", "srv": "23%", "1vx": "0", "plant": "5", "hs": "56%"},
{"name": "Harp3r", "rating": "1.08", "kd": "35-30 (+5)", "entry": "8-3 (+5)", "kost": "66%", "kpr": "0.80", "srv": "32%", "1vx": "0", "plant": "1", "hs": "55%"}, 
{"name": "aLx3inE", "rating": "1.04", "kd": "29-24 (+5)", "entry": "3-4 (-1)", "kost": "70%", "kpr": "0.66", "srv": "45%", "1vx": "0", "plant": "0", "hs": "61%"}
]
palyer_s_list = []
for player_stats in data:
    name = player_stats["name"]
    kd = player_stats["kd"].split("(")[0]
    entry = player_stats["entry"].split("(")[0]
    kost = player_stats["kost"].split("%")[0]
    kpr = player_stats["kpr"]
    srv = player_stats["srv"].split("%")[0]
    onevx = player_stats["1vx"]
    plant = player_stats["plant"]
    hs = player_stats["hs"].split("%")[0]
    k = kd.split("-")[0]
    d = kd.split("-")[1]
    entry_k = entry.split("-")[0]
    entry_d = entry.split("-")[1]

    player_score = float(k)*10 + float(d)*8 + float(entry_k)*10 + float(entry_d)*8 + float(kost) + float(srv) + float(onevx)*15 + float(plant)*15

    player_dic  = {name: player_score}
    palyer_s_list.append(player_dic)
#     player_dic = {
#     "name" : name,
#     "kost" : float(kost),
#     "kpr" : float(kpr),
#     "srv" : float(srv),
#     "Onevx" : float(Onevx),
#     "plant" : float(plant),
#     "hs" : float(hs),
#     "k" : float(k),
#     "d" : float(d),
#     "entry_k" : float(entry_k),
#     "entry_d" : float(entry_d)
#     }
#     palyer_s_list.append(player_dic)

print(palyer_s_list)
