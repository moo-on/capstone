#볼린저 밴드 추세추종 전략 시간봉 데이터
import numpy as np
import datetime
import sys
sys.path.insert(0, '/capstone/time')
import pandas as pd

df = pd.read_csv('hourly_btc.csv', encoding='euc-kr')
df.index = pd.to_datetime(df['시간'])

df = df[df.index >= datetime.datetime(2017,10,1)]
for k in np.arange(6,10,0.5):
    df['MA20'] = df['종가'].rolling(window=20).mean()
    df['stddev'] = df['종가'].rolling(window=20).std()
    df['upper'] = df['MA20'] + (df['stddev'] * 2)
    df['lower'] = df['MA20'] - (df['stddev'] * 2)
    df['PB'] = (df['종가'] - df['lower']) / (df['upper'] - df['lower'])
    df['TP'] = (df['고가'] + df['저가'] + df['종가']) / 3
    df['PMF'] = 0
    df['NMF'] = 0
    df['buy'] = 0
    df['buyTarget'] = 0
    df['sellTarget'] = 0
    df['range'] = (df['고가'] - df['저가']) * 0.1
    df['target'] = df['시가'] + df['range'].shift(1)

    for i in range(len(df.종가)-1):
        if df.TP.values[i] < df.TP.values[i+1]:
            df.PMF.values[i+1] = df.TP.values[i+1] * df.거래량.values[i+1]
            df.NMF.values[i+1] = 0
        else:
            df.NMF.values[i+1] = df.TP.values[i+1] * df.거래량.values[i+1]
            df.PMF.values[i+1] = 0
    df['MFR'] = df.PMF.rolling(window=10).sum() / df.NMF.rolling(window=10).sum()
    df['MFI10'] = 100 - 100 / (1 + df['MFR'])

    for i in range(len(df.종가)-1):
        if df.buy.values[i] == 0:
            if df.PB.values[i] > (k * 0.1) and df.MFI10.values[i] > (k * 10):
                df.buyTarget.values[i] = df.종가.values[i]
                df.buy.values[i+1] = 1
            else:
                df.buyTarget.values[i] = 0
        else:
            if df.PB.values[i] < ((10-k) * 0.1) and df.MFI10.values[i] < ((10 - k) * 10):
                df.buyTarget.values[i] = df.buyTarget.values[i-1]
                df.sellTarget.values[i] = df.종가.values[i]
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