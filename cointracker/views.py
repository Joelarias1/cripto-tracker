from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
import requests


# Create your views here.
cg = CoinGeckoAPI()

def welcome(request):
    topcoins = get_top_coins()
    trending = get_trending_coins()
    exchgvolume = get_exchanges()
    return render(request, "cointracker/welcome.html", {"coins":topcoins, "trending":trending, "exchange":exchgvolume})


def get_top_coins():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=10, page=1, sparkline=False)
    for coin in coins:
        coin['current_price'] = '${:,.2f}'.format(coin['current_price'])
        coin['market_cap'] = '${:,.2f}'.format(coin['market_cap'])
    return coins



#Cards de HTML
def get_trending_coins():
    cg = CoinGeckoAPI()
    trending_coins = cg.get_search_trending()['coins'][:10]
    return trending_coins


def get_exchanges():
  # Hacer la llamada a la API
  response = requests.get("https://api.coingecko.com/api/v3/exchanges?per_page=10&page=1")

  if response.status_code == 200:
    data = response.json()
    exchanges = []

    # Iterar a través de cada exchange en la lista de exchanges
    for exchange in data:
      # Agregar el exchange a la lista
      exchanges.append(exchange)

    return exchanges
  else:
    return []