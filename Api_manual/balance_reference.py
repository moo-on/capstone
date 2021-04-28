import pybithumb
import time
import security
bithumb = security.bithumb

# class 생성
balance = bithumb.get_balance("BTC")  # 코인잔고 /거래 중 코인 수 /보유 중 총 원화 /주문에 사용 된 원화


for ticker in pybithumb.get_tickers():
    balance = bithumb.get_balance(ticker)
    print(ticker, ':', balance)
    time.sleep(0.1)

