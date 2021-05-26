#볼린저 밴드 추세추종 기법
import sys
sys.path.insert(0, '/Users/I/capstone/capstone/backtesting')
import numpy as np
import byperiod_backtesting as bp


def get_ror_V_MA(k):
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

    for i in range(len(df.close) - 1):
        if df.buy.values[i] == 0:
            if df.PB.values[i] < ((10 - k) * 0.1):  # %b가 0.7보다 작으면
                df.buyTarget.values[i] = df.close.values[i]
                df.buy.values[i + 1] = 1
            else:
                df.buyTarget.values[i] = 0
        else:
            if df.PB.values[i] > (k * 0.1):                                             # %b가 0.7보다 면
                df.buyTarget.values[i] = df.buyTarget.values[i - 1]
                df.sellTarget.values[i] = df.close.values[i]
                df.buy.values[i + 1] = 0
            else:
                df.buyTarget.values[i] = df.buyTarget.values[i - 1]
                df.sellTarget.values[i] = 0
                df.buy.values[i + 1] = 1
    fee = 0.0032
    df['ror'] = np.where((df['buyTarget'] > 0) & (df['sellTarget'] > 0),
                         df['sellTarget'] / df['buyTarget'] - fee,
                         1)
    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    print("%b가 ", (10 - k) * 0.1, "보다 작을 때 사고")
    print("%b가 ", (k * 0.1), "보다 클 때 판다")
    print("MDD: ", df['dd'].max())
    print("HPR: ", df['hpr'][-2])
    print("")
    return df['hpr'][-2]

for j in range(1,10):
    df = bp.period_df(j).copy()                             # df1 ~ df9까지
    print('period : ', j)
    for k in np.arange(6, 10, 0.5):                         # k 값 세팅
        print("%.1f " % (k))
        ror = get_ror_V_MA(k)
        print("")

'''
MDD:  22.281315088834504
HPR:  22.218279342102626
'''