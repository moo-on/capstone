import sys
sys.path.insert(0, 'C:/Users/Jun/PycharmProjects/capstone/backtesting')
import pybithumb
import numpy as np
import datetime
import copy
import pandas as pd


df = pybithumb.get_ohlcv("eth")
df_ori = copy.deepcopy(df[df.index >= datetime.datetime(2017,10,1)])


# df = pd.read_csv('data/hourly_eth.csv', encoding='euc-kr')
# df.drop('Unnamed: 0',axis = 1, inplace = True)
# df['시간'] = pd.to_datetime(df['시간'])
# df.set_index('시간', inplace = True)
# df.columns = ['open', 'high', 'low', 'close', 'volume']
# df_ori = copy.deepcopy(df)


up = [[datetime.datetime(2017,10,1),datetime.datetime(2018,1,14)],
      [datetime.datetime(2019,4,3),datetime.datetime(2019,8,13)],
      [datetime.datetime(2020,10,11),datetime.datetime(2021,4,21)]]

down =[[datetime.datetime(2018,1,15),datetime.datetime(2018,4,20)],
      [datetime.datetime(2018,11,14),datetime.datetime(2019,1,6)],
      [datetime.datetime(2021,4,22),datetime.datetime(2021,4,28)]]

mid =[[datetime.datetime(2018,4,21),datetime.datetime(2018,11,13)],
      [datetime.datetime(2019,1,7),datetime.datetime(2019,4,2)],
      [datetime.datetime(2019,8,14),datetime.datetime(2020,10,10)]]

periods = [up] + [down] + [mid]

def period_df(n):
   if n == 1: return df_ori[(df_ori.index >= up[0][0]) & (df_ori.index <= up[0][1])]
   if n == 2: return df_ori[(df_ori.index >= up[1][0]) & (df_ori.index <= up[1][1])]
   if n == 3: return df_ori[(df_ori.index >= up[2][0]) & (df_ori.index <= up[2][1])]
   if n == 4: return df_ori[(df_ori.index >= down[0][0]) & (df_ori.index <= down[0][1])]
   if n == 5: return df_ori[(df_ori.index >= down[1][0]) & (df_ori.index <= down[1][1])]
   if n == 6: return df_ori[(df_ori.index >= down[2][0]) & (df_ori.index <= down[2][1])]
   if n == 7: return df_ori[(df_ori.index >= mid[0][0]) & (df_ori.index <= mid[0][1])]
   if n == 8: return df_ori[(df_ori.index >= mid[1][0]) & (df_ori.index <= mid[1][1])]
   if n == 9: return df_ori[(df_ori.index >= mid[2][0]) & (df_ori.index <= mid[2][1])]
   else : return 'error'







if __name__ == "__main__":
    print('good')
    # 변동성
    # def get_ror(k=0.5):
    #     df = pybithumb.get_ohlcv("BTC")
    #     df = df[(df.index >= lst[0]) & (df.index <= lst[1])]
    #     df['range'] = (df['high'] - df['low']) * k
    #     df['target'] = df['open'] + df['range'].shift(1)
    #
    #     fee = 0.0032
    #     df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
    #     ror = df['ror'].cumprod()[-2]
    #     return ror
    #
    # for lst in mid:
    #     print(lst[0])
    #     df = pybithumb.get_ohlcv("BTC")
    #
    #
    #     for k in np.arange(0.1, 1.0, 0.1):
    #         ror = get_ror(k)
    #         print("%.1f " % (k))
    #         print(" %f" % (ror))
    #
    #
    #
    # #변동성 이평선
    #
    #
    # df = pybithumb.get_ohlcv("BTC")
    # df = df[(df.index >= lst[0]) & (df.index <= lst[1])]
    #
    # for lst in mid:
    #     print(lst[0])
    #     df = pybithumb.get_ohlcv("BTC")
    #     df = df[(df.index >= lst[0]) & (df.index <= lst[1])]
    #
    #     for k in np.arange(0.1, 1.0, 0.1):
    #         df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
    #         df['range'] = (df['high'] - df['low']) * k
    #         df['target'] = df['open'] + df['range'].shift(1)
    #         df['bull'] = df['open'] > df['ma5']
    #         fee = 0.0032
    #         df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
    #
    #         df['hpr'] = df['ror'].cumprod()
    #         df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    #         print("%.1f, %.4f" % (k, df['hpr'][-2]))
    #         # print("MDD: ", df['dd'].max())
    #         # print("HPR: ", df['hpr'][-2])
    #         print("")