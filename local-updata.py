import requests

r = requests.get('http://localhost:9080/crawl.json?url=https://siege.gg/matches&spider_name=upcomingm')

data = (r.json())['items']
print(data)
