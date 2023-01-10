from django.http import JsonResponse
from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
import requests


# Create your views here.
cg = CoinGeckoAPI()

def welcome(request):
    topcoins = get_top_coins()
    trending = get_trending_coins()
    exchgvolume = get_exchanges()
    ath = get_top_coins_with_ath()
    return render(request, "cointracker/welcome.html", {"coins":topcoins, "trending":trending, "exchange":exchgvolume, "ath":ath})


def get_top_coins():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=15, page=1, sparkline=False)
    for coin in coins:
        coin['current_price'] = '${:,.2f}'.format(coin['current_price'])
        coin['market_cap'] = '${:,.0f}'.format(coin['market_cap'])
        coin['high_24h'] = '${:,.2f}'.format(coin['high_24h'])
        coin['low_24h'] = '${:,.2f}'.format(coin['low_24h'])
    return coins



#Cards de HTML
def get_trending_coins():
    cg = CoinGeckoAPI()
    trending_coins = cg.get_search_trending()['coins'][:10]
    return trending_coins


def get_exchanges():
  response = requests.get("https://api.coingecko.com/api/v3/exchanges?per_page=10&page=1")

  if response.status_code == 200:
    data = response.json()
    exchanges = []

    for exchange in data:
      exchanges.append(exchange)

    return exchanges
  else:
    return []


def get_top_coins_with_ath():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=30, page=1, sparkline=False)
    for coin in coins:
        coin['current_price'] = '${:,.2f}'.format(coin['current_price'])
        coin['ath'] = '${:,.2f}'.format(coin['ath'])
        coin['ath_change_percentage'] = '{:,.2f}%'.format(coin['ath_change_percentage'])
    return coins



def coin_detail(request, coin_id):
    cg = CoinGeckoAPI()
    coin_data = cg.get_coin_by_id(coin_id)

    current_price = float(coin_data['market_data']['current_price']['usd'])

    if current_price >= 0.001:
        current_price = '${:,.2f}'.format(current_price)
    else:
        current_price = '${:,.10f}'.format(current_price)

    market_cap = '${:,.0f}'.format(coin_data['market_data']['market_cap']['usd'])
    
    if request.method == 'POST':
        # Si el usuario ha enviado una cantidad de tokens, se calcula el valor en USD de la cantidad ingresada
        current_price = current_price.replace('$', '').replace(',', '')
        token_amount = float(request.POST['token_amount'])
        usd_amount = token_amount * float(current_price)
        usd_amount = '${:,.2f}'.format(usd_amount)
    else:
        # Si el usuario no ha enviado una cantidad de tokens, simplemente muestras el precio actual del token
        usd_amount = current_price

    return render(request, 'cointracker/coin-detail.html', {'coin': coin_data, 'current_price': current_price, 'market_cap': market_cap, 'usd_amount': usd_amount})







  
  
