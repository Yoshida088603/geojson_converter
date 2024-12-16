# Geojson converter
geojson_converter.exe は、PotreeDesktopから出力された３次元ポリゴンのJsonファイルをGeojson形式に変換するためのプログラムです。

# How to Use
geojson_converter.exeをダウンロードします（インストール不要）
PotreeDesktopで、日本の平面直角座標系で作成された点群（LAS/LAZ)を読み込み、3次元ポリゴンを作成し、これをjsonファイルとして出力します。
PotreeDesktopから出力したjsonファイルを、geojson_converter.exeにドラッグアンドドロップして、ダイアログに従って適切なEPSGコード（例: 茨城県 = EPSG:6677)を選択し、OKボタンを押します。
PotreeDesktopから出力されたjsonファイルと同じディレクトリに、geojson形式（EPSG:3857）に変換された３次元ポリゴンの情報が出力されます。
