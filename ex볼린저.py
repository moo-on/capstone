import pybithumb
import numpy as np
import pyupbit
import datetime

df = pybithumb.get_ohlcv("BTC")
df = df[df.index >= datetime.datetime(2017,10,1)]

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
df['TP'] = (df['high'] + df['low'] + df['close']) / 3
df['PMF'] = 0
df['NMF'] = 0


#buy가 1이면 살 수 있는 상태 sell이 1이면 팔 수 있는 상태

trade_buy = True
trade_sell = False

df['buy'] = np.where(df['lower'] > df['low'],1,0 )
df['sell'] = np.where(df['upper'] <df['high'],1, 0)

def trade_buy_f(row):
    global trade_buy
    global trade_sell
    if (trade_buy == True) and (row.buy == 1):
        trade_buy = False
        trade_sell = True
        return 1
    else:
        if row.sell ==1:
            trade_buy = True
        return 0


def trade_sell_f(row):
    global trade_buy
    global trade_sell
    if (trade_sell == True) and (row.sell == 1):
        trade_sell = False
        trade_buy = True
        return 1
    else:
        if row.buy ==1:
            trade_sell = True
        return 0

df['trade_buy'] =df.apply(trade_buy_f, axis = 1)
trade_sell = False
df['trade_sell'] =df.apply(trade_sell_f, axis = 1)

lst_buy = df[df.trade_buy==1]
lst_sell = df[df.trade_sell==1]

#lst buy가 하나 더 구해져서 팔아지지는 않아서 하나 더 김.


hpr = []
for sell, buy in zip(lst_sell['upper'], lst_buy['lower']):
    ror = sell/buy
    hpr.append(ror)



