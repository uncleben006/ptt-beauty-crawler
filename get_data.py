import requests

url = "https://api-ptt-beauty.herokuapp.com/api/"

response = requests.get(url)
datas = response.json()

for data in datas:
    print(data)