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