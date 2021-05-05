#볼린저밴드 반전 매매기법
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

df['II'] = (2*df['close']-df['high']-df['low'])/(df['high']-df['low'])*df['volume']
df['IIP21'] = df['II'].rolling(window=21).sum()/df['volume'].rolling(window=21).sum()*100 #21일 기간 동안의 II합을 21일 기간 동안의 거래량 합으로 나누어 표준화한 것
df = df.dropna()

# 그래프 그리기
plt.figure(figsize=(9, 9))
plt.subplot(3, 1, 1)
plt.title('SK Hynix Bollinger Band(20 day, 2 std) - Reversals')
plt.plot(df.index, df['close'], 'm', label='Close')
plt.plot(df.index, df['upper'], 'r--', label ='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label ='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:       # ①
        plt.plot(df.index.values[i], df.close.values[i], 'r^')  # ②
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:     # ③
        plt.plot(df.index.values[i], df.close.values[i], 'bv')  # ④
plt.legend(loc='best')

plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'], 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')

plt.subplot(3, 1, 3)
plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')
for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^') # ⑤
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv') # ⑥
plt.grid(True)
plt.legend(loc='best')
plt.show()
#여기까지

df['buy'] = 0
df['buyTarget'] = 0
df['sellTarget'] = 0

for i in range(len(df.close)-1):
    if df.buy.values[i] == 0:
        if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
            df.buyTarget.values[i] = df.close.values[i]
            df.buy.values[i+1] = 1
        else:
            df.buyTarget.values[i] = 0

    else:
        if df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
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

df.to_excel("larry_ma_Reversals.xlsx")