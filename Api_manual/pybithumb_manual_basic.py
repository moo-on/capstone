import pybithumb
import time

tickers = pybithumb.get_tickers() #코인 정보


price = pybithumb.get_current_price("BTC") #현재 가격 #ALL
print(price)

detail = pybithumb.get_market_detail("BTC") #저가 고가 거래금액 거래량

orderbook = pybithumb.get_orderbook("BTC")
# bids매수호가  ask매도호가

bids = orderbook['bids'] # quantity, price #호가

all = pybithumb.get_current_price('ALL') # 211pg
for k,v in all.items():
    print(k, v['closing_price'])