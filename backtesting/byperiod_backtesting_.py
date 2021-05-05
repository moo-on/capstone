import sys
sys.path.insert(0, 'C:/Users/Jun/PycharmProjects/capstone/backtesting')
import pybithumb
import numpy as np
import datetime
import V_MA_backtesting as M
import copy


df = pybithumb.get_ohlcv("BTC")
df_ori = copy.deepcopy(df[df.index >= datetime.datetime(2017,10,1)])

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

def by_period(periods, function, find_hyperparameter):
    for period in periods:
        for lst_ in period:
            for lst in lst_:
                df = df_ori[(df_ori.index >= lst[0]) & (df_ori.index <= lst[1])]
                M.find_hyperparameter(function)
                print("_____________________")

def period_df(periods,function):
    for period in periods:
        for lst in period:
            print(lst[0],"~~",lst[1])
            df = df_ori[(df_ori.index >= lst[0]) & (df_ori.index <= lst[1])]



by_period(periods, M.get_ror_V_MA ,M.find_k)


df_lst = []
for period in periods:
    for lst in period:
        print(lst[0],"~~",lst[1])
        df = df_ori[(df_ori.index >= lst[0]) & (df_ori.index <= lst[1])]
        df_lst.append(df)



if __name__ == "__main__":
    #변동성
    def get_ror(k=0.5):
        df = pybithumb.get_ohlcv("BTC")
        df = df[(df.index >= lst[0]) & (df.index <= lst[1])]
        df['range'] = (df['high'] - df['low']) * k
        df['target'] = df['open'] + df['range'].shift(1)

        fee = 0.0032
        df['ror'] = np.where(df['high'] > df['target'], df['close'] / df['target'] - fee, 1)
        ror = df['ror'].cumprod()[-2]
        return ror

    for lst in mid:
        print(lst[0])
        df = pybithumb.get_ohlcv("BTC")


        for k in np.arange(0.1, 1.0, 0.1):
            ror = get_ror(k)
            print("%.1f " % (k))
            print(" %f" % (ror))



    #변동성 이평선


    df = pybithumb.get_ohlcv("BTC")
    df = df[(df.index >= lst[0]) & (df.index <= lst[1])]

    for lst in mid:
        print(lst[0])
        df = pybithumb.get_ohlcv("BTC")
        df = df[(df.index >= lst[0]) & (df.index <= lst[1])]

        for k in np.arange(0.1, 1.0, 0.1):
            df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
            df['range'] = (df['high'] - df['low']) * k
            df['target'] = df['open'] + df['range'].shift(1)
            df['bull'] = df['open'] > df['ma5']
            fee = 0.0032
            df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)

            df['hpr'] = df['ror'].cumprod()
            df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
            print("%.1f, %.4f" % (k, df['hpr'][-2]))
            # print("MDD: ", df['dd'].max())
            # print("HPR: ", df['hpr'][-2])
            print("")