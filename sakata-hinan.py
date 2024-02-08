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

data = pd.read_csv('data/hinan.csv')
sakata_data = data[(data['都道府県名及び市町村名'] == '山形県酒田市')]

marker_cluster = MarkerCluster(
    name='sakata hinan',
    overlay=True,
    control=False,
    icon_create_function=None
)

types = [
  { 'key': '洪水', 'fileName': 'hinan/floodData.html' },
  { 'key': '崖崩れ、土石流及び地滑り', 'fileName': 'hinan/landslideData.html' },
  { 'key': '高潮', 'fileName': 'hinan/stormSurgeData.html' },
  { 'key': '地震', 'fileName': 'hinan/earthquakeData.html' },
  { 'key': '津波', 'fileName': 'hinan/tsunamiData.html' },
  { 'key': '大規模な火事', 'fileName': 'hinan/fireData.html' },
  { 'key': '内水氾濫', 'fileName': 'hinan/inlandFloodingData.html' },
]

for type in types:
  filtered_data = sakata_data[sakata_data[type['key']] == 1]

  for _, row in filtered_data.iterrows():
    marker = folium.Marker([row['緯度'], row['経度']])
    popup = f"""
    <div id="popup">
      <h3>{row['施設・場所名']}</h3>
      <p><b>住所</b> {replace_nan(row['住所'])}</p>
      <p><b>備考</b> {replace_nan(row['備考'])}</p>
    </div>
    """
    folium.Popup(popup).add_to(marker)
    marker_cluster.add_child(marker)

  marker_cluster.add_to(map)

  map.save(type["fileName"])

  with open(type["fileName"], 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

  link = soup.new_tag('link', rel="stylesheet", href="../main.css")
  soup.head.append(link)

  title = soup.new_tag('title')
  title.string = f"{type['key']} | 山形県酒田市 指定緊急避難場所マップ"
  soup.head.append(title)

  link = soup.new_tag('link', rel="stylesheet", href="../main.css")
  soup.head.append(link)

  header = soup.new_tag('h1')
  header.string = f"山形県酒田市 指定緊急避難場所マップ（{type['key']}）"
  soup.body.insert(0, header)

  attribution = f"""
  <p id="attribution">この「山形県酒田市 指定緊急避難場所マップ（{type['key']}）」は、「指定緊急避難場所の全国データ(公開している市区町村)」(国土地理院)(https://www.gsi.go.jp/bousaichiri/hinanbasho.html#info2)を加工して作成しています。</p>
  """
  soup.body.append(BeautifulSoup(attribution, 'html.parser'))

  with open(type["fileName"], 'w', encoding='utf-8') as file:
    file.write(str(soup))

