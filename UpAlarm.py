import pybithumb
# 가상화폐 티커 목록 얻기
tickers = pybithumb.get_tickers()
print(tickers)
print(len(tickers))

""" 현재가 얻기
import time

tickers = pybithumb.get_tickers()
for ticker in tickers:
    price = pybithumb.get_current_price(ticker)
    print(ticker, price)
    time.sleep(0.1)
"""

# 거래소 거래 정보
detail = pybithumb.get_market_detail("BTC")
print(detail)

# 호가
orderbook = pybithumb.get_orderbook("BTC")
print(orderbook)

for k in orderbook:
    print(k)

import datetime
orderbook = pybithumb.get_orderbook("BTC")
ms = int(orderbook["timestamp"])

dt = datetime.datetime.fromtimestamp(ms/1000)
print(dt)

orderbook = pybithumb.get_orderbook("BTC")
bids = orderbook['bids']
asks = orderbook['asks']

for bid in bids:
    price = bid['price']
    quant = bid['quantity']
    print("매수호가: ", price, "매수잔량: ", quant)

for ask in asks:
    price = ask['price']
    quant = ask['quantity']
    print("매도호가: ", price, "매도잔량: ", quant)

# 여러 가상화폐에 대한 정보 한번에 얻기
all = pybithumb.get_current_price("ALL")
for k, v in all.items():
    print(k, v)

for ticker, data in all.items():
    print(ticker, data['closing_price'])

#예외 처리
price = {"open": 100, 'high': 150, 'low': 90, 'close': 130}
print("point-1")
try:
    open = price['open1']
except:
    pass
print("print-2")

"""
import time

while True:
    price = pybithumb.get_current_price("BTC")
    if price is not None:
        print(price/10)
    
    #이렇게 예외처리 가
    try:
        print(price/10)
    :except:
        print("에러 발생", price)
    
    time.sleep(0.2)
"""

# 상승장 알리미(1)
btc = pybithumb.get_ohlcv("BTC")
close = btc['close']
print((close[0] + close[1] + close[2] + close[3] + close[4]) / 5)
print((close[1] + close[2] + close[3] + close[4] + close[5]) / 5)
print((close[2] + close[3] + close[4] + close[5] + close[6]) / 5)

window = close.rolling(5)
ma5 = window.mean()
# ma5 = close.rolling(5).mean() 와 같다
print(ma5)

def bull_market(ticker):
    df = pybithumb.get_ohlcv(ticker)
    ma5 = df['close'].rolling(5).mean()
    price = pybithumb.get_current_price(ticker)
    last_ma5 = ma5[-2]

    if price > last_ma5:
        return True
    else:
        return False

tickers = pybithumb.get_tickers()
for ticker in tickers:
    is_bull = bull_market("BTC")
    if is_bull :
        print(ticker, " 상승장")
    else:
        print(ticker, " 하락장")