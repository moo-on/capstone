#변동성 전략 시간봉 데이터
import numpy as np
import datetime
import sys
sys.path.insert(0, '/capstone/time')
import pandas as pd

df = pd.read_csv('hourly_btc.csv', encoding='euc-kr')
df.index = pd.to_datetime(df['시간'])

df = df[df.index >= datetime.datetime(2017,10,1)]
for k in np.arange(1,10,1):
    df['range'] = (df['고가'] - df['저가']) * k
    df['target'] = df['시가'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['고가'] > df['target'],
                         df['종가'] / df['target'] - fee,
                         1)

    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    print(df['hpr'][-2])