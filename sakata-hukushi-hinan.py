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

data = pd.read_csv('https://www.city.sakata.lg.jp/shisei/opendata/opendata_hinanjo.files/fukushihinanjo.csv', encoding="cp932")

marker_cluster = MarkerCluster(
    name='sakata hukushi hinan',
    overlay=True,
    control=False,
    icon_create_function=None
)

for _, row in data.iterrows():
  marker = folium.Marker([row['緯度'], row['経度']])
  popup = f"""
    <div style='width: 100px'>
      <h3>{row['名称']}</h3>
      <a href="http://local.google.co.jp/maps?q={row['緯度']},{row['経度']}"  target="_blank" rel="noopener noreferrer">Googleマップで表示</a>
    </div>"""
  folium.Popup(popup).add_to(marker)
  marker_cluster.add_child(marker)

marker_cluster.add_to(map)

map.save('sakata-hukushi-hinan.html')

with open('sakata-hukushi-hinan.html', 'r', encoding='utf-8') as file:
  soup = BeautifulSoup(file, 'html.parser')

title = soup.new_tag('title')
title.string = "山形県酒田市福祉避難所マップ"
soup.head.append(title)

link = soup.new_tag('link', rel="stylesheet", href="main.css")
soup.head.append(link)

title = soup.new_tag('h1')
title.string = "山形県酒田市福祉避難所マップ"
soup.body.insert(0, title)

text = """
<p id="attribution">この「山形県酒田市福祉避難所マップ」は、酒田市オープンデータの指定緊急避難場所・指定避難所・福祉避難所、酒田市、クリエ
イティブ・コモンズ・ライセンス 表示 4.0 国際ライセンスを利用しています。
（https://creativecommons.org/licenses/by/4.0/deed.ja）</p>
"""
soup.body.append(BeautifulSoup(text, 'html.parser'))

with open('sakata-hukushi-hinan.html', 'w', encoding='utf-8') as file:
  file.write(str(soup))
