import pybithumb
import time
import security
bithumb = security.bithumb


order = bithumb.buy_limit_order("BTC", 100000, 0.01)
print(order) # ex) bid(매수), 코인, 주문번호

time.sleep(10)
cancel = bithumb.cancel_order(order)
print(cancel) #성공 시 True