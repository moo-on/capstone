import pybithumb
import time

con_key = 'a5c306a25f33167a6f678f040e21e82c'
sec_key = '713a64bcb71fd745099d2a50faef250a'

bithumb = pybithumb.Bithumb(con_key, sec_key)

# class 생성
balance = bithumb.get_balance("BTC") # 코인잔고,거래 중 코인 수량, 보유 중 총 원화, 주문에 사용 된 원화

for ticker in pybithumb.get_tickers():
    balance = bithumb.get_balance(ticker)
    print(ticker, ':', balance)
    time.sleep(0.1)

# **매수**

# 지정가매수
order = bithumb.buy_limit_order("BTC", 10000000, 0.01) -> (티커, 지정가, 매수 수량) *최소주문수량,유효자릿수(소수점 넷째),호가단위(ex 비트코인은 천원 단위)
print(order) -> (주문종류, 티커, 주문번호)

# 시장가매수
## order = bithumb.buy_market_order("BTC", 1) -> (티커, 매수 수량) *최소주문수량과 유효자릿수
# 수량 맞추는법(시장가)
## krw = bithumb.get_balance("BTC")[2]
## orderbook = pybithumb.get_orderbook("BTC")
## asks = orderbook['asks']
## sell_price = ask[0]['price']
## unit = krw/sell_price
## print(unit)

# **매도**

# 지정가매도
## order =bithumb.sell_limit_order("BTC", 100000000, 1) #천만원에 하나 사겠다.
## print(order)

#보유중인 수량만큼 지정가 매도

