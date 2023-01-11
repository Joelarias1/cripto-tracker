from django.http import JsonResponse
from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
import requests
import plotly.graph_objects as go


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
    graph_div = graph30days(coin_id)

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
        # Si el usuario no ha enviado una cantidad de tokens, se muestra el valor actual
        usd_amount = current_price

    return render(request, 'cointracker/coin-detail.html', {'coin': coin_data, 'current_price': current_price, 'market_cap': market_cap, 'usd_amount': usd_amount, 'graph_div': graph_div})



def graph30days(coin_id):
    cg = CoinGeckoAPI()

    # Obtener los datos históricos de la moneda
    coin_history = cg.get_coin_market_chart_by_id(coin_id, vs_currency='usd', days='30', interval='daily')

    # Extraer los precios máximos para cada día
    max_prices = [data[1] for data in coin_history['prices']]

    # Crear el gráfico de línea utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1,31)), y=max_prices, name='Max Price',mode='lines+markers'))
    fig.update_layout(title='Price History (Last 30 Days)', xaxis_title='Days', yaxis_title='Price (USD)',showlegend=True)

    # Crear una cadena que contenga los datos del gráfico en formato HTML
    graph_div = fig.to_html(full_html=False, config={"modeBarButtonsToRemove": ['toImage', 'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']})

    return graph_div







  
  
