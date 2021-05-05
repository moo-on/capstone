#볼린저 밴드 밑에서 사서 위에서 팔기
import pybithumb
import numpy as np
import datetime

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
        if df.close.values[i] < df.lower.values[i]:
            df.buyTarget.values[i] = df.close.values[i]
            df.buy.values[i+1] = 1
        else:
            df.buyTarget.values[i] = 0

    else:
        if df.close.values[i] > df.upper.values[i]:
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




# #buy가 1이면 살 수 있는 상태 sell이 1이면 팔 수 있는 상태
#
# trade_buy = True
# trade_sell = False
#
# df['buy'] = np.where(df['lower'] > df['low'], 1, 0)
# df['sell'] = np.where(df['upper'] < df['high'], 1, 0)
#
# def trade_buy_f(row):
#     global trade_buy
#     global trade_sell
#     if (trade_buy == True) and (row.buy == 1):
#         trade_buy = False
#         trade_sell = True
#         return 1
#     else:
#         if row.sell ==1:
#             trade_buy = True
#         return 0
#
# def trade_sell_f(row):
#     global trade_buy
#     global trade_sell
#     if (trade_sell == True) and (row.sell == 1):
#         trade_sell = False
#         trade_buy = True
#         return 1
#     else:
#         if row.buy ==1:
#             trade_sell = True
#         return 0
#
# df['trade_buy'] =df.apply(trade_buy_f, axis = 1)
# trade_sell = False
# df['trade_sell'] =df.apply(trade_sell_f, axis = 1)
#
# lst_buy = df[df.trade_buy==1]
# lst_sell = df[df.trade_sell==1]
#
# #lst buy가 하나 더 구해지고 팔아지지는 않아서 하나 더 김.
#
# hpr = []
# hpr_ = 1
# fee = 0.0032
#
# for sell, buy in zip(lst_sell['upper'], lst_buy['lower']):
#     ror = sell/buy
#     hpr_ *= (ror - fee)
#     hpr.append(ror)
#
# print("hpr : ", hpr_)


df.to_excel("larry_ma_j.xlsx")