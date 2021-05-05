import pybithumb
import numpy as np
import datetime

df = pybithumb.get_ohlcv("BTC")
df = df[df.index >= datetime.datetime(2017,10,1)]
fee = 0.0032

def get_ror_V(k):
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
    ror = df['ror'].cumprod()[-2]
    return ror

for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror_V(k)
    print("%.1f " % (k))
    print(" %f" % (ror))

'''
전체기간 : 0.8
상승장 : 0.1, 0.2
하락장 : 0.5, 0.7
횡보장 : 0.9
'''

