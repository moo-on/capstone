#볼린저 밴드 기본 매매전 밴드폭 별 각 장별 시간봉 데이터
import sys
sys.path.insert(0, '/Users/I/capstone/capstone/time')
import numpy as np
import byperiod_backtesting_timedata as bp


def get_ror_V_MA(k):
    df['range'] = (df['고가'] - df['저가']) * k
    df['target'] = df['시가'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['고가'] > df['target'],
                         df['종가'] / df['target'] - fee,
                         1)

    df['hpr'] = df['ror'].cumprod()
    df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
    print("%.4f " % (df['hpr'][-2]))
    return df['hpr'][-2]

for j in range(1,10):
    df = bp.period_df(j).copy()
    print('period : ', j)
    for k in np.arange(1, 10, 1):
        print("%.1f " % (k))
        ror = get_ror_V_MA(k)


