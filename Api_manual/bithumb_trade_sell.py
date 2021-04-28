import pybithumb
import time
import security

bithumb = security.bithumb


# **매도**

# 지정가매도
order = bithumb.sell_limit_order("BTC", 100000000, 1) #천만원에 하나 팔겠다. -> 1개 없으면 에러
print(order)

# 보유중인 수량만큼 지정가 매도
unit = bithumb.get_balance("BTC")[0] # 코인잔고,거래 중 코인 수량, 보유 중 총 원화, 주문에 사용 된 원화
order = bithumb.sell_limit_order("BTC, 99000000000000, unit") # 지정가매도, 코인, 주문번호 -> 호가가격단위 1000원

# 시장가 매도
unit = bithumb.get_balance("BTC")[0]
order = bithumb.sell_market_order("BTC", unit)   #전부 시장가 매도
