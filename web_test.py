import requests
from bs4 import BeautifulSoup

def get_per(code):
    url = "https://finance.naver.com/item/main.nhn?code=" + code #sk 하이닉스 주가
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    tags = soup.select("#_per")
    tag = tags[0]
    return float(tag.text)

def get_dividend(code):
    url = "https://finance.naver.com/item/main.nhn?code=" + code
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    tags = soup.select("#_dvr")
    tag = tags[0]
    return float(tag.text)

print(get_per("000660"))      #PER
print(get_dividend("000660")) #배당수익률

