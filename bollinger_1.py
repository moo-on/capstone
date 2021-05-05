import pybithumb
import numpy as np
import datetime

df1 = pybithumb.get_ohlcv("BTC")
df = df1[df1.index >= datetime.datetime(2017,10,1)]

df['MA20'] = df['close'].rolling(window=20).mean().shift(1)
df['stddev'] = df['close'].rolling(window=20).std().shift(1)
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['target'] = np.where((df['lower'] > df['low']),
                        df['lower'],
                        df['MA20'])

fee = 0.0032
df['ror'] = np.where((df['high'] > df['upper']),
                    df['upper'] / df['target'] - fee,
                    1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma_bollinger.xlsx")
