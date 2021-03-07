#DataFrame 생성
from pandas import DataFrame
from pandas import Series

data = {'open': [737, 750], "high": [755, 780], "low":[700, 710], "close": [750, 770]}
df = DataFrame(data)

#volume이란 이름으로 Series 객체를 추가
s = Series([300, 400])
df["volume"] = s
print(df)
#연산을 이용하여 Series 객체 추가
upper = df["open"] * 1.3
df["upper"] = upper
print(df)

df = DataFrame(data , index=["2018-01-01", "2018-01-02"])
print(df)
print(df.loc["2018-01-01"]) #loc 메서드에 특정 인데스 넘겨주면 해당하는 행의 데이터가 Series로 변환
print(df.iloc[0])           #iloc 메서드를 사용하면 자동으로 맵핑 되는 숫자 인덱스로 값을 얻을 수 있음

target = ["2018-01-01", "2018-01-02"]
print(df.loc[target])

target = [0, 1]             #위 코드와 같다.
print(df.iloc[target])

#excel을 이용하여 DataFrame 생성
import pandas as pd
df = pd.read_excel("ohlc.xlsx")
df = df.set_index('date')
#df.to_excel("ohlc-2.xlsx") ohlc-2.xlsx 이름의 엑셀 파일로 DataFrame 객체 저장
print(df)

#칼럼 시프트  shift(1) 값을 하나 내려줌 shift(-1) 값을 하나 올려줌
s = Series([100, 200, 300])
s2 = s.shift(-1)
print(s)
print(s2)