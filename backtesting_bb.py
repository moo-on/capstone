import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC")

bb_size = 20
pb = 2

df['ma20'] = df['close'].rolling(window=bb_size).mean().shift(1)
df['std20'] = df['close'].rolling(window=bb_size).std().shift(1)
df['upper bollingerBand'] = df['ma20'] + pb * df['std20']
df['down bollingerBand'] = df['ma20'] - pb * df['std20']

df['range'] = (df['high'] - df['low']) * 0.6
df['target'] = df['open'] + df['range'].shift(1)
df['bull'] = df['open'] > df['ma20']

fee = 0.0032
df['ror'] = np.where((df['high'] > df['target']) & df['bull'],
                    df['close'] / df['target'] - fee,
                    1)

df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])
df.to_excel("larry_ma_bb.xlsx")