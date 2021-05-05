import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC")
df['range'] = (df['high'] - df['low']) * 0.5
df['range_shigt1'] = df['range'].shift(1)
df['target'] = df['open'] + df['range'].shift(1)
df.to_excel("btc.xlsx")