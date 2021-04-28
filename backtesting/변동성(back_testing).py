import pybithumb
import numpy as np
import datetime

df = pybithumb.get_ohlcv("BTC")
df = df[df.index >= datetime.datetime(2017,10,1)]

def get_ror(k=0.5):
    df = pybithumb.get_ohlcv("BTC")
    df = df[df.index >= datetime.datetime(2017, 10, 1)]
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f " % (k))
    print(" %f" % (ror))