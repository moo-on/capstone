import sys
sys.path.insert(0, 'C:/Users/Jun/PycharmProjects/capstone/backtesting')
import pybithumb
import numpy as np
import pyupbit
import datetime
import byperiod_backtesting as bp



def get_ror_V_MA(k = 0.5):
    fee = 0.0032
    df['ma5'] = df['close'].rolling(window=5).mean().shift(1)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)
    df['bull'] = df['open'] > df['ma5']

    df['ror'] = np.where((df['high'] > df['target']) & df['bull'], df['close'] / df['target'] - fee, 1)
    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    #print("hpr:", df['hpr'][-2])
    return df['hpr'][-2]



for i in range(1,10):
    df = bp.period_df(1).copy() # df1 ~ df9까지
    print('period : ',i)
    for k in np.arange(0.1, 1.0, 0.1): # k 값 세팅
        ror = get_ror_V_MA(k)
        print("%.1f " % (k))
        print("%f" % (ror))




if __name__ == "__main__":

    df = pybithumb.get_ohlcv("BTC")
    df = df[df.index >= datetime.datetime(2017,10,1)]

    get_ror_V_MA()



'''
전체기간 : 0.2
상승장 : 0.1 & 0.2
하락장 : 0.8, 0.5 _ 변동성 크게 잡는게 유리
횡보장 : 0.9
'''


#print(df['high'].iloc[-1]/df['high'].iloc[1])