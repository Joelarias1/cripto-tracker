from django.http import JsonResponse
from django.shortcuts import render
from pycoingecko import CoinGeckoAPI
import requests
import plotly.graph_objects as go


# def welcome(request):
#     cg = CoinGeckoAPI()
#     #Exchange Count
#     url = 'https://api.coingecko.com/api/v3/exchanges'
#     response = requests.get(url)
#     total_exchanges = response.headers
        
#     #CryptoCount
#     crypto_count = cg.get_global()

#     #Return
#     context = {'exchange': total_exchanges, 'crypto_count': crypto_count}
#     return render(request, "cointracker/welcome.html", context)


def welcome(request):

    return render(request, "cointracker/welcome.html")



def coinlist(request):
    # cg = CoinGeckoAPI()
    # exchanges = cache.get('exchanges_list')
    # if exchanges is None:
    #     # Si los datos no están en cache, obtenerlos de la API
    #     exchanges = cg.get_exchanges_list()
    #     # Guardar los datos en cache con una clave 'exchanges_list'
    #     cache.set('exchanges_list', exchanges, 3600)  # guardar en cache durante 1 hora
    # # Procesar los datos para mostrar en la vista
    # for exchange in exchanges:
    #     exchange_id = exchange['id']
    #     exchange_data = cg.get_exchanges_by_id(exchange_id)
    #     exchange['centralized'] = exchange_data['centralized']
    # context = {'exchanges': exchanges}
    
    return render(request, 'cointracker/coin-list.html')





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


def get_top_coins_with_ath():
    cg = CoinGeckoAPI()
    coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=30, page=1, sparkline=False)
    for coin in coins:
        coin['current_price'] = '${:,.2f}'.format(coin['current_price'])
        coin['ath'] = '${:,.2f}'.format(coin['ath'])
        coin['ath_change_percentage'] = '{:,.2f}%'.format(coin['ath_change_percentage'])
    return coins



#Funciones Vista Coin-Detail:
def coin_detail(request, coin_id):
    cg = CoinGeckoAPI()
    coin_data = cg.get_coin_by_id(coin_id)
    graph_div = graph30days(coin_id)
    tickers = get_exchanges_by_coin_id(coin_id)

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

    return render(request, 'cointracker/coin-detail.html', {'coin': coin_data, 'current_price': current_price, 'market_cap': market_cap, 'usd_amount': usd_amount, 'graph_div': graph_div, 'tickers': tickers})



#Listado de exchanges que venden la moneda
def get_exchanges_by_coin_id(coin_id):
    cg = CoinGeckoAPI()
    ticker = cg.get_coin_ticker_by_id(coin_id, order='trust_score_desc, volume_desc', include_exchange_logo=True, depth=True)
    
    for data in ticker["tickers"]:
        data["volume"] = "${:,.0f}".format(data["volume"])
        if data["last"] < 0.001:
            data['last'] = "${:,.10f}".format(data["last"])
        else:
            data['last'] = "${:,.2f}".format(data["last"])
    return ticker


#Grafico
def graph30days(coin_id):
    cg = CoinGeckoAPI()
    coin_history = cg.get_coin_market_chart_by_id(coin_id, vs_currency='usd', days='30', interval='daily')
    max_prices = [data[1] for data in coin_history['prices']]

    # Crear el gráfico de línea utilizando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1,31)), y=max_prices, name='Max Price',mode='lines+markers'))
    fig.update_layout(title='Price History (Last 30 Days)', xaxis_title='Days', yaxis_title='Price (USD)',showlegend=False)

    # Crear una cadena que contenga los datos del gráfico en formato HTML
    graph_div = fig.to_html(full_html=False, config={"modeBarButtonsToRemove": ['toImage', 'zoom2d', 'pan2d', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d']})

    return graph_div







  
  
