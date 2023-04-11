import requests
import re
from bs4 import BeautifulSoup 
import time
import yfinance as yf
import datetime
#para las small caps en eeuu que tenian ttm/y-3 >3 lo dejaste en 4200
#para las small capps de eeuu que tenian ttm/y-3 < 3 y yoy >20% lo dejaste en 4750
#para small caps en munich hasta 5625

def anti_ban():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sleeptime = 180 - datetime.datetime.utcnow().second
    time.sleep(sleeptime)

def scrape_web(url):
    with requests.session():
        header = {'Connection': 'keep-alive',
                   'Expires': '-1',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) \
                   AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
                   }
        website = requests.get(url, headers=header)
        return BeautifulSoup(website.text, 'html.parser')

def pick_all_tickers(x, link):
    stocks = []
    #de vez en cuando el link cambia
    url = f'{link}?count=25&offset={x}'
    print(url)
    soup = scrape_web(url)
    classes = soup.find_all(class_='Fw(600) C($linkColor)')
    for class_ in classes:
        stocks.append(class_.text)
    return stocks

def convert_to_float(spans, symbol):
    return float(spans[1].text.replace(symbol,'')), float(spans[2].text.replace(symbol,'')), float(spans[3].text.replace(symbol,'')), float(spans[4].text.replace(symbol,''))

def filter_stock(ticker, filtered_stocks, stocks_scores):
    ##################################   ESTO ES PARA DECIR QUE QUIERO SOLO LAS QUE LA ACCION HAYA SUBIDO   #######################################################
    '''
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.datetime.now() - datetime.timedelta(days=365*5)).strftime('%Y-%m-%d')
    stock_history = yf.download(ticker, start=start_date, end=end_date)
    ulti = stock_history.head(1)
    primi = stock_history.tail(1)

    try:
        if primi['Open'][0] < ulti['Open'][0]:
            return filtered_stocks, stocks_scores
    except:
        print('falla el download')
        return filtered_stocks, stocks_scores
    '''
    ###############################################################################################################################################################
    url = f'https://finance.yahoo.com/quote/{ticker}/financials?p={ticker}'
    soup = scrape_web(url)
    classes = soup.find_all(class_='D(tbr) fi-row Bgc($hoverBgColor):h')
    try:
        spans = classes[0].find_all('span')
    except:
        print('me cago en el yahoo')
        return filtered_stocks, stocks_scores
    try:
        if ',' in spans[1].text:
            ttm, y_1, y_2, y_3 = convert_to_float(spans, ',')
        else:
            ttm, y_1, y_2, y_3 = convert_to_float(spans, '.')
        if ttm>=y_1 and y_1>(y_2*1.2) and y_2>(y_3*1.2):
            filtered_stocks[stock] = {'ttm':ttm, 'y-1':y_1, 'y-2':y_2, 'y-3':y_3}
            stocks_scores[stock] = ttm/y_3
            print(f'redimiendo de {ttm/y_3}')
    except:
        print('me cago en la empresa')
        return filtered_stocks, stocks_scores
    return filtered_stocks, stocks_scores

############################################################################################################################
#######################   llena estas 3 variables y crea una carpeta con "screener_name" de nombre   #######################
x_total = 9000
x_ini = 6650
link = 'https://finance.yahoo.com/screener/unsaved/ffbeb559-3dcc-4bd6-94b1-0e174ecf764e'
screener_name = 'eeuu'
############################################################################################################################

for x_actual in range(x_ini, x_total, 25):
    now = datetime.datetime.now()
    current_time_1 = now.strftime("%H:%M:%S")
    print("Current Time =", current_time_1)
    filtered_stocks, stocks_scores = {}, {}
    stocks = pick_all_tickers(x_actual, link)
    for stock in stocks:
        print(stock)
        filtered_stocks, stocks_scores = filter_stock(stock, filtered_stocks, stocks_scores)
    if len(stocks_scores) != 0:
        with open(f'{screener_name}/{screener_name}_{x_actual}.txt', 'w') as f:
            for line in stocks_scores:
                f.write(line)
                f.write('\n')
    now = datetime.datetime.now()
    current_time_2 = now.strftime("%H:%M:%S")
    dt_format = '%H:%M:%S'
    time_diff = datetime.datetime.strptime(current_time_2, dt_format) - datetime.datetime.strptime(current_time_1, dt_format)
    seconds_diff = int(time_diff.total_seconds())
    print("Current Time =", current_time_2, 'PAUSA (s):', 120 - seconds_diff)
    time.sleep(180 - seconds_diff)
