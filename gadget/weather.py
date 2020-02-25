
from urllib.request import urlopen
from bs4 import BeautifulSoup


url = urlopen('https://tianqi.moji.com/weather/china/beijing/haidian-district')
soup = BeautifulSoup(url, 'html.parser')


alert = soup.find('div', class_="wea_alert clearfix").em
print("空气质量：" + alert.string)

weather = soup.find('div', class_="wea_weather clearfix")
print("当前温度：" + weather.em.string)
print("天气：" + weather.b.string)

