# Geojson Converter
geojson_converter.exe は、PotreeDesktopで作成された3次元ポリゴンのJSONファイルをGeoJSON形式に変換するためのプログラムです。

# 使用方法
## プログラムの準備
geojson_converter.exe をダウンロードしてデスクトップなど、分かりやすい場所に保存します（インストールは不要です）。
![スクリーンショット 2024-12-16 191628](https://github.com/user-attachments/assets/162b2f6d-4a9e-4540-82e4-43504c117d53)


## PotreeDesktopでの事前準備
日本の平面直角座標系で作成された点群（LAS/LAZ）をPotreeDesktopに読み込みます。
PotreeDesktopで3次元ポリゴンを作成し、JSONファイルとして出力します。
![スクリーンショット 2024-12-16 181831](https://github.com/user-attachments/assets/c6c93b26-b3fb-46c0-b281-66d0bd02d09c)

## JSONファイルの変換
出力したJSONファイルを geojson_converter.exe にドラッグ＆ドロップします。
表示されたダイアログで、対応するEPSGコードを選択します（例: 茨城県 = EPSG:6677）。
「OK」ボタンを押します。
![スクリーンショット 2024-12-16 183105](https://github.com/user-attachments/assets/5fdc5333-ccc1-4018-9c14-2fbbd1f3830f)


## 変換後のファイル
JSONファイルと同じディレクトリに、GeoJSON形式（EPSG:3857） に変換された3次元ポリゴンデータが保存されます。
保存されたGeojsonファイルはQGIなど一般的なGISソフトウェアで読込・表示が可能です。
![スクリーンショット 2024-12-16 183854](https://github.com/user-attachments/assets/c10190c6-105f-4085-9752-fa1de4f75b52)
