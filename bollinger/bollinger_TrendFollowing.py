#볼린저 밴드 추세추종 기법
import pybithumb
import numpy as np
import datetime

for k in np.arange(6,10,0.5):
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

    for i in range(len(df.close)-1):
        if df.buy.values[i] == 0:
            if df.PB.values[i] > (k * 0.1) and df.MFI10.values[i] > (k * 10):   #%b가 0.7보다 크고 10일 기준 MFI가 70보다 크면
                df.buyTarget.values[i] = df.close.values[i]
                df.buy.values[i+1] = 1
            else:
                df.buyTarget.values[i] = 0
        else:
            if df.PB.values[i] < ((10-k) * 0.1) and df.MFI10.values[i] < ((10 - k) * 10):   #%b가 0.7보다 작고 10일 기준 MFI가 30보다 작으면
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
    print("%b가 ", (k*0.1) ,"보다 크고 10일 기준 MFI가 ", k*10, "보다 클때 사고")
    print("%b가 ", (10-k) * 0.1, "보다 작고 10일 기준 MFI가 ", (10-k) * 10, "보다 작을때 팔았을때")
    print("MDD: ", df['dd'].max())
    print("HPR: ", df['hpr'][-2])
    print("")

# df.to_excel("bollinger/larry_ma_TrendFollowing.xlsx")

'''
MDD:  22.281315088834504
HPR:  22.218279342102626
'''