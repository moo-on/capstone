import pybithumb
import time
import security
bithumb = security.bithumb



# **매수**

# 지정가매수
order = bithumb.buy_limit_order("BTC", 10000000, 0.01) #-> (티커, 지정가, 매수 수량(최소주문수량, 유효자릿수)) *호가단위(ex 비트코인은 천원 단위)
print(order) #-> (주문종류, 티커, 주문번호)    ex) bid(매수), 'coin_name', order_number

# 시장가매수
order = bithumb.buy_market_order("BTC", 1) #-> (티커, 매수 수량) *최소주문수량과 유효자릿수

# 최우선 매도 호가 수량 맞추는법 + 주문(시장가)
krw = bithumb.get_balance("BTC")[2] # 보유중 총 원화
orderbook = pybithumb.get_orderbook("BTC")
asks = orderbook['asks']
sell_price = asks[0]['price']
unit = krw/sell_price
order = bithumb.buy_market_order("BTC", unit)




