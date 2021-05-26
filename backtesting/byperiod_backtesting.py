import sys
sys.path.insert(0, '/Users/I/capstone/capstone/backtesting')
import pybithumb
import datetime
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
