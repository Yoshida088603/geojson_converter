#Geojson Converter
geojson_converter.exe は、PotreeDesktopで作成された3次元ポリゴンのJSONファイルをGeoJSON形式に変換するためのプログラムです。

#使用方法
##プログラムの準備
geojson_converter.exe をダウンロードします（インストールは不要です）。

##PotreeDesktopでの事前準備
日本の平面直角座標系で作成された点群（LAS/LAZ）をPotreeDesktopに読み込みます。
PotreeDesktopで3次元ポリゴンを作成し、JSONファイルとして出力します。

##JSONファイルの変換
出力したJSONファイルを geojson_converter.exe にドラッグ＆ドロップします。
表示されたダイアログで、対応するEPSGコードを選択します（例: 茨城県 = EPSG:6677）。
「OK」ボタンを押します。

##変換後のファイル
JSONファイルと同じディレクトリに、GeoJSON形式（EPSG:3857） に変換された3次元ポリゴンデータが保存されます。
