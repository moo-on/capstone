import pybithumb
import numpy as np
import datetime

df = pybithumb.get_ohlcv("BTC")
df1 = df[df.index >= datetime.datetime(2017,10,1)]

df['MA20'] = df['close'].rolling(window=20).mean().shift(1)
df['stddev'] = df['close'].rolling(window=20).std().shift(1)
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['target'] = np.where((df['lower'] > df['close']),
                        df['close'],
                        #여기에 어떻게 넣어야 되나 이말이지
                        ).shift(1)
df['bull'] = df['open'] > df['MA20']

fee = 0.0032
df['ror'] = np.where((df['close'] > df['upper']) & df['bull'],
                    df['close'] / df['target'],
                    1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma_bollinger.xlsx")
