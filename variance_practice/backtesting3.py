import pybithumb
import numpy as np
import datetime

df = pybithumb.get_ohlcv("BTC")
#df2 = df1[df1.index >= datetime.datetime(2017,10,1)]
#df = df2[df2.index <= datetime.datetime(2018,1,14)]

df['ma5'] = df['close'].rolling(5).mean().shift(1)
df['range'] = (df['high'] - df['low']) * 0.6
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma5']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                    df['close'] / df['target'] - fee,
                    1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
#df.to_excel("larry_ma.xlsx")