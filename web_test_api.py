import requests
import datetime

r = requests.get("https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=btc_krw")
bitcoin = r.json()

timestamp = bitcoin['timestamp']
date = datetime.datetime.fromtimestamp((timestamp/1000))
print(date)

print(bitcoin)
print(type(bitcoin))
print(bitcoin['last'])
print(bitcoin['bid'])
print(bitcoin['ask'])
print(bitcoin['volume'])