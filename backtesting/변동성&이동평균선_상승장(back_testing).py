import pybithumb
import numpy as np
import pyupbit
import datetime

df = pybithumb.get_ohlcv("BTC")
df = df[df.index >= datetime.datetime(2017,10,1)]
fee = 0.0032

def get_ror_V_MA(k):
    df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['bull'] = df['open'] > df['ma5']

    df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    return df['hpr'][-2]

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror_V_MA(k)
    print("%.1f " % (k))
    print(" %f" % (ror))

print(df['high'].iloc[-1]/df['high'].iloc[1])

'''
전체기간 : 0.2
상승장 : 0.1 & 0.2
하락장 : 0.8, 0.5 _ 변동성 크게 잡는게 유리
횡보장 : 0.9
'''


