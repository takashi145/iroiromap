import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import folium
from folium.plugins import MarkerCluster

def replace_nan(value):
  return '-----' if pd.isna(value) else value

map = folium.Map(
  location=[38.9147, 139.8365], 
  height=500, 
  zoom_start=11
)

folium.plugins.LocateControl(
  auto_start=False,
  strings={
    "title": "現在地を表示",
    "popup": "現在地"
  }
).add_to(map)

folium.plugins.Fullscreen(
    position="topright",
    title="Expand me",
    title_cancel="Exit me",
    force_separate_button=True,
).add_to(map)

data = pd.read_csv('https://www.city.sakata.lg.jp/shisei/opendata/opendata_aed.files/R5.12saisin.csv', encoding="cp932")

marker_cluster = MarkerCluster(
    name='sakata aed',
    overlay=True,
    control=False,
    icon_create_function=None
).add_to(map)

for _, row in data.iterrows():
  marker = folium.Marker(
    location=[row['緯度'], row['経度']],
    icon=folium.CustomIcon(
      icon_image="./images/aed.png",
      icon_size=(30, 30),
    )
  ).add_to(map)

  popup = f"""
  <div id="popup">
    <h3>{row['設置場所']}</h3>
    <p><b>住所</b> {replace_nan(row['住所'])}</p>
    <p><b>電話番号</b> {replace_nan(row['電話番号'])}</p>
    <p><b>設置位置</b> {replace_nan(row['設置位置'])}</p>
    <p><b>台数</b> {replace_nan(row['台数'])}</p>
    <p><b>備考</b> {replace_nan(row['備考'])}</p>
    <a href="http://local.google.co.jp/maps?q={row['住所']}" target="_blank" rel="noopener noreferrer">Googleマップで表示</a>
  </div>
  """
  folium.Popup(popup).add_to(marker)
  marker_cluster.add_child(marker)

map.save('sakata-aed.html')

with open('sakata-aed.html', 'r', encoding='utf-8') as file:
  soup = BeautifulSoup(file, 'html.parser')

title = soup.new_tag('title')
title.string = "山形県酒田市AEDマップ"
soup.head.append(title)

link = soup.new_tag('link', rel="stylesheet", href="main.css")
soup.head.append(link)

title = soup.new_tag('h1')
title.string = "山形県酒田市AEDマップ"
soup.body.insert(0, title)

text = """
<p id="attribution">この「山形県酒田市AEDマップ」は、酒田市オープンデータの酒田市所管施設AED設置状況、酒田市、クリエ
イティブ・コモンズ・ライセンス 表示 4.0 国際ライセンスを利用しています。
（https://creativecommons.org/licenses/by/4.0/deed.ja）</p>
"""
soup.body.append(BeautifulSoup(text, 'html.parser'))

with open('sakata-aed.html', 'w', encoding='utf-8') as file:
  file.write(str(soup))
