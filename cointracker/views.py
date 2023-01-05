from django.shortcuts import render
import requests



# Create your views here.

def welcome(request):
    data = getApi()
    coins = get_coins()
    return render(request, "cointracker/welcome.html", {"data": data, "coins": coins})

def getApi():
    url = "https://api.coingecko.com/api/v3/ping"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error {response.status_code}: {response.text}"
    
def get_coins():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1&sparkline=false"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return f"Error {response.status_code}: {response.text}"