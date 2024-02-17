import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import folium
from folium.plugins import MarkerCluster

def replace_nan(value):
  return '-----' if pd.isna(value) else value

map = folium.Map(
  location=[38.2554,140.3396], 
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

data = pd.read_csv('https://www.pref.yamagata.jp/documents/1570/public_toilet.csv', encoding="shift-jis")

marker_cluster = MarkerCluster(
    name='yamagata toilet',
    overlay=True,
    control=False,
    icon_create_function=None
)

for _, row in data.iterrows():
  marker = folium.Marker([row['緯度'], row['経度']])
  popup = f"""
  <div id="popup">
    <h3><ruby>{row['名称']}<rt>{row['名称_カナ']}</rt></ruby></h3>
    <p><b>都道府県名又は市町村名</b> {replace_nan(row['都道府県名又は市町村名'])}</p>
    <p><b>住所</b> {replace_nan(row['住所'])}</p>
    <p><b>設置位置</b> {replace_nan(row['設置位置'])}</p>
    <p><b>備考</b> {replace_nan(row['備考'])}</p>
    <a href="http://local.google.co.jp/maps?q={row['住所']}"  target="_blank" rel="noopener noreferrer">Googleマップで表示</a>
  </div>
  """
  folium.Popup(popup).add_to(marker)
  marker_cluster.add_child(marker)

marker_cluster.add_to(map)

map.save('yamagata-toilet.html')

with open('yamagata-toilet.html', 'r', encoding='utf-8') as file:
  soup = BeautifulSoup(file, 'html.parser')

title = soup.new_tag('title')
title.string = "山形県公衆トイレマップ"
soup.head.append(title)

link = soup.new_tag('link', rel="stylesheet", href="main.css")
soup.head.append(link)

title = soup.new_tag('h1')
title.string = "山形県公衆トイレマップ"
soup.body.insert(0, title)

text = """
<p id="attribution">この「山形県 公衆トイレマップ」は以下の著作物を改変して利用しています。公衆トイレ一覧、山形県、クリエ
イティブ・コモンズ・ライセンス 表示 4.0 国際
（https://creativecommons.org/licenses/by/4.0/deed.ja）</p>
"""
soup.body.append(BeautifulSoup(text, 'html.parser'))

with open('yamagata-toilet.html', 'w', encoding='utf-8') as file:
  file.write(str(soup))
