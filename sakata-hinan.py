import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import folium
from folium.plugins import MarkerCluster, GroupedLayerControl

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

data = pd.read_csv('data/hinan.csv')
sakata_data = data[(data['都道府県名及び市町村名'] == '山形県酒田市')]

types = ["洪水", "崖崩れ、土石流及び地滑り", "高潮", "地震", "津波", "大規模な火事", "内水氾濫"]

groups = []
for type in types:
  filtered_data = sakata_data[sakata_data[type] == 1]
  group = folium.FeatureGroup(name=type)
  groups.append(group)

  marker_cluster = MarkerCluster(
    name=type,
    overlay=True,
    control=False,
    icon_create_function=None
  )

  for _, row in filtered_data.iterrows():
    marker = folium.Marker(
      [row['緯度'], row['経度']], 
      tags=[type]
    )
    popup = f"""
    <div id="popup">
      <h3>{row['施設・場所名']}</h3>
      <p><b>住所</b> {replace_nan(row['住所'])}</p>
      <p><b>備考</b> {replace_nan(row['備考'])}</p>
      <a href="http://local.google.co.jp/maps?q={row['住所']}"  target="_blank" rel="noopener noreferrer">Googleマップで表示</a>
    </div>
    """
    folium.Popup(popup).add_to(marker)
    marker.add_to(marker_cluster)
    marker_cluster.add_to(group)
    
  map.add_child(group)

GroupedLayerControl(
  groups={'災害': groups},
  collapsed=False,
).add_to(map)

map.save("hinan.html")

with open("hinan.html", 'r', encoding='utf-8') as file:
  soup = BeautifulSoup(file, 'html.parser')

link = soup.new_tag('link', rel="stylesheet", href="main.css")
soup.head.append(link)

title = soup.new_tag('title')
title.string = f"山形県酒田市 指定緊急避難場所マップ"
soup.head.append(title)

link = soup.new_tag('link', rel="stylesheet", href="../main.css")
soup.head.append(link)

header = soup.new_tag('h1')
header.string = f"山形県酒田市 指定緊急避難場所マップ"
soup.body.insert(0, header)

attribution = f"""
<p id="attribution">この「山形県酒田市 指定緊急避難場所マップ」は、「指定緊急避難場所の全国データ(公開している市区町村)」(国土地理院)(https://www.gsi.go.jp/bousaichiri/hinanbasho.html#info2)を加工して作成しています。</p>
"""
soup.body.append(BeautifulSoup(attribution, 'html.parser'))

with open("hinan.html", 'w', encoding='utf-8') as file:
  file.write(str(soup))

