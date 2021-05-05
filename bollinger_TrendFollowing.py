import pybithumb
import numpy as np
import datetime
import matplotlib.pyplot as plt

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
df['buy'] = 0
df['buyTarget'] = 0
df['sellTarget'] = 0

for i in range(len(df.close)-1):
    if df.TP.values[i] < df.TP.values[i+1]:
        df.PMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.NMF.values[i+1] = 0
    else:
        df.NMF.values[i+1] = df.TP.values[i+1] * df.volume.values[i+1]
        df.PMF.values[i+1] = 0
df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
df['MFI10'] = 100 - 100 / (1 + df['MFR'])

# 그래프
plt.figure(figsize=(9,8))
plt.subplot(2, 1, 1)
plt.title('BitCoin')
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
plt.legend(loc='best')

plt.subplot(2, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show()
# 여기까지

for i in range(len(df.close)-1):
    if df.buy.values[i] == 0:
        if df.PB.values[i] > 0.7 and df.MFI10.values[i] > 70:
            df.buyTarget.values[i] = df.close.values[i]
            df.buy.values[i+1] = 1
        else:
            df.buyTarget.values[i] = 0
    else:
        if df.PB.values[i] < 0.3 and df.MFI10.values[i] < 30:
            df.buyTarget.values[i] = df.buyTarget.values[i-1]
            df.sellTarget.values[i] = df.close.values[i]
            df.buy.values[i+1] = 0
        else:
            df.buyTarget.values[i] = df.buyTarget.values[i-1]
            df.sellTarget.values[i] = 0
            df.buy.values[i+1] = 1

fee = 0.0032
df['ror'] = np.where((df['buyTarget'] > 0) & (df['sellTarget'] > 0),
                    df['sellTarget'] / df['buyTarget'] - fee,
                    1)
df['hpr'] = df['ror'].cumprod()
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD: ", df['dd'].max())
print("HPR: ", df['hpr'][-2])

df.to_excel("larry_ma_TrendFollowing.xlsx")