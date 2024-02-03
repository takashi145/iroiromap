import pandas as pd
from io import StringIO
from bs4 import BeautifulSoup
import folium

def replace_nan(value):
  return '-----' if pd.isna(value) else value

map = folium.Map(
  location=[38.2554,140.3396], 
  height=500, 
  zoom_start=11
)

data = pd.read_csv('https://www.pref.yamagata.jp/documents/1570/public_toilet.csv', encoding="shift-jis")

for _, row in data.iterrows():
  popup=f"""
  <div id="popup">
    <h3><ruby>{row['名称']}<rt>{row['名称_カナ']}</rt></ruby></h3>
    <p><b>住所</b> {replace_nan(row['住所'])}</p>
    <p><b>設置位置</b> {replace_nan(row['設置位置'])}</p>
    <p><b>備考</b> {replace_nan(row['備考'])}</p>
  </div>
  """

  folium.Marker(
    [row['緯度'], row['経度']], 
    popup=popup,
    # icon=folium.Icon(color="green")
  ).add_to(map)

map.save('yamagata-toilet.html')

with open('yamagata-toilet.html', 'r', encoding='utf-8') as file:
  soup = BeautifulSoup(file, 'html.parser')

link = soup.new_tag('link', rel="stylesheet", href="main.css")
soup.head.append(link)

title = soup.new_tag('h1')
title.string = "山形県 公衆トイレマップ"
soup.body.insert(0, title)

text = """
<p id="attribution">この「山形県 公衆トイレマップ」は以下の著作物を改変して利用しています。公衆トイレ一覧、山形県、クリエ
イティブ・コモンズ・ライセンス 表示 4.0 国際
（https://creativecommons.org/licenses/by/4.0/deed.ja）</p>
"""
soup.body.append(BeautifulSoup(text, 'html.parser'))

with open('yamagata-toilet.html', 'w', encoding='utf-8') as file:
  file.write(str(soup))
