import pyupbit
import time
import datetime

access_key = "lqo1onHdUKyzuOFgxPHnl8FjxPlgnvJkwGrSNjWy"
secret_key = "A87jhQhVJETu397ab0bQFgcxxG5wz4pV1oA3lC4l"

upbit = pyupbit.Upbit(access_key, secret_key)

def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker)
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    return target

def buy_crypto_currency(ticker):
    krw = upbit.get_balance(ticker)[2]
    orderbook = pyupbit.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    upbit.buy_market_order(ticker, unit)

def sell_crypto_currency(ticker):
    unit = upbit.get_balance(ticker)[0]
    upbit.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(5).mean()
    return ma[-2]

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
ma5 = get_yesterday_ma5("KRW-BTC")
target_price = get_target_price("KRW-BTC")

#매수 매도 시도
while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("KRW-BTC")
            sell_crypto_currency("KRW-BTC")

        current_price = pyupbit.get_current_price("KRW-BTC")
        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("KRW-BTC")
    except:
        print("에러발생")
    time.sleep(1)