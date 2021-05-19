import sys
sys.path.insert(0, 'C:/Users/Jun/PycharmProjects/capstone/backtesting')
import pybithumb
import numpy as np
import pyupbit
import datetime
import byperiod_backtesting as bp
import pandas as pd

#전체기간
df = pybithumb.get_ohlcv("xrp")
df = df[df.index >= datetime.datetime(2017,10,1)]

#시간봉
df = pd.read_csv('data/hourly_btc.csv', encoding='euc-kr')
df.drop('Unnamed: 0',axis = 1, inplace = True)
df.set_index('시간', inplace = True)
df.columns = ['open', 'high', 'low', 'close', 'volume']


##
trade_buy = True
trade_sell = False
##

def get_df(small, big):
    global trade_sell
    def trade_buy_f(row):
        global trade_buy
        global trade_sell
        if (trade_buy == True) and (row.buy == 1):
            trade_buy = False
            trade_sell = True
            return 1
        else:
            if row.sell == 1:
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
            if row.buy == 1:
                trade_sell = True
            return 0

    fee = 0.0032
    df['ma3'] = df['close'].rolling(window=small, min_periods=1).mean().shift(1)
    df['ma7'] = df['close'].rolling(window=big, min_periods=1).mean().shift(1)
    df['down'] = np.where(df['ma3'].shift(1) < df['ma7'].shift(1), 1, 0)
    df['up'] = np.where(df['ma3'].shift(1) > df['ma7'].shift(1), 1, 0)
    df['buy'] = np.where((df['down'].shift(1) ==1) & (df['up'] == 1) , 1, 0)
    df['sell'] = np.where((df['up'].shift(1) == 1) & (df['down'] == 1), 1, 0)

    df['trade_buy'] = df.apply(trade_buy_f, axis=1)
    trade_sell = False
    df['trade_sell'] = df.apply(trade_sell_f, axis=1)

##
def get_ror():
    lst_buy = list(df.open[df.trade_buy == 1])
    lst_sell = list(df.open[df.trade_sell == 1])
    if len(lst_buy) > len(lst_sell): lst_buy.pop()
    if len(lst_buy) == 0 or len(lst_sell) == 0:
        lst_buy.append(1)
        lst_sell.append(1)
    hpr = []
    for sell, buy in zip(lst_sell, lst_buy):
        ror = sell / buy
        hpr.append(ror)

    hpr = pd.Series(hpr).cumprod()
    ror = hpr.iloc[-1]
    return ror

##
get_df(1,32)
ror = get_ror()
print(ror)

dic = []
for s in range(1,51):
    for b in range(1,101):
        get_df(s,b)
        ror = get_ror()
        dic.append(ror)
        #print(s)
        #print(b)
        #print(ror)

print(max(dic))

print('d')



for i in range(1,10):
    trade_buy = True
    trade_sell = False
    df = bp.period_df(i).copy() #df1 ~ df9까지
    print('period : ',i)
    get_df(3, 7)
    ror = get_ror()
    print("ror:%.4f" %(ror))
    print("__________")


