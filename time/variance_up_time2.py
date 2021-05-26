#변동성 + 상스장 전략 변도옥 별 기간  시간봉 데이터
import sys
sys.path.insert(0, '/Users/I/capstone/capstone/time')
import numpy as np
import byperiod_backtesting_timedata as bp


def get_ror_V_MA(k):
    df['ma5'] = df['종가'].rolling(5).mean().shift(1)
    df['range'] = (df['고가'] - df['저가']) * k
    df['target'] = df['시가'] + df['range'].shift(1)
    df['bull'] = df['시가'] > df['ma5']

    fee = 0.0032
    df['ror'] = np.where((df['고가'] > df['target']) & df['bull'],
                         df['종가'] / df['target'] - fee,
                         1)

    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    #print("%.4f " % (df['hpr'][-2]))
    return df['hpr'][-2]

for j in range(1,10):
    df = bp.period_df(j).copy()
    print('period : ', j)
    for k in np.arange(1, 10, 1):
        ror = get_ror_V_MA(k)
        print("%.1f, " % (k) + "%.4f" % (ror))



