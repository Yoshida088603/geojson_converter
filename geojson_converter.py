import logging
import datetime
import os
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon, Point
from shapely.ops import orient
from shapely.geometry import mapping
import json
import tkinter as tk
from tkinter import ttk
import sys

# ログファイルの設定を修正
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except Exception as e:
        # ログディレクトリが作れない場合は、カレントディレクトリを使用
        log_dir = os.path.join(os.getcwd(), 'logs')
        os.makedirs(log_dir, exist_ok=True)

current_time = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = os.path.join(log_dir, f'geojson_conversion_{current_time}.log')

# ログの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()  # コンソールにも出力
    ]
)

# ファイルのドラッグアンドドロップで取得する
def get_input_file():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        if not os.path.exists(input_path):
            print(f"エラー: ファイルが見つかりません: {input_path}")
            sys.exit(1)
        return input_path
    else:
        print("GeoJSONファイルをドラッグアンドドロップしてください。")
        sys.exit(1)

# ダイアログを作成
def select_epsg():
    root = tk.Tk()
    root.title("EPSGコード選択")

    # メインフレーム
    frame = ttk.Frame(root, padding=10)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # ラベル
    label = ttk.Label(frame, text="日本の平面直角座標系（JGD2011）のEPSGコードを選択してください:")
    label.grid(row=0, column=0, sticky=tk.W, pady=5)

    # コンボボックス
    options = [f"EPSG:{epsg} - {area}" for _, (epsg, area) in epsg_codes_jgd2011.items()]
    selected_value = tk.StringVar()
    combo = ttk.Combobox(frame, textvariable=selected_value, values=options, state="readonly", width=50)
    combo.grid(row=1, column=0, sticky=tk.W, pady=5)
    combo.current(0)  # デフォルト値

    # OKボタン
    def on_ok():
        root.selected_epsg = int(combo.get().split(":")[1].split(" ")[0])  # EPSGコードを抽出
        root.destroy()

    button = ttk.Button(frame, text="OK", command=on_ok)
    button.grid(row=2, column=0, pady=10)

    root.mainloop()
    return root.selected_epsg

# 日本の平面直角座標系（JGD2011）のEPSGコードと適用区域
epsg_codes_jgd2011 = {
    1: (6669, "長崎県、鹿児島県の一部"),
    2: (6670, "福岡県、佐賀県、熊本県、大分県、宮崎県、鹿児島県の一部"),
    3: (6671, "山口県、島根県、広島県"),
    4: (6672, "香川県、愛媛県、徳島県、高知県"),
    5: (6673, "兵庫県、鳥取県、岡山県"),
    6: (6674, "京都府、大阪府、福井県、滋賀県、三重県、奈良県、和歌山県"),
    7: (6675, "石川県、富山県、岐阜県、愛知県"),
    8: (6676, "新潟県、長野県、山梨県、静岡県"),
    9: (6677, "東京都、福島県、栃木県、茨城県、埼玉県、千葉県、群馬県、神奈川県"),
    10: (6678, "青森県、秋田県、山形県、岩手県、宮城県"),
    11: (6679, "北海道の一部（小樽市、函館市など）"),
    12: (6680, "北海道の一部"),
    13: (6681, "北海道の一部（北見市、帯広市など）"),
    14: (6682, "東京都の一部（南方諸島）"),
    15: (6683, "沖縄県の一部"),
    16: (6684, "沖縄県の一部"),
    17: (6685, "沖縄県の一部"),
    18: (6686, "東京都の一部（南方諸島）"),
    19: (6687, "東京都の一部（南方諸島）")
}

# 入力ファイルを取得（ハードコードされたパスを削除）
input_geojson = get_input_file()
output_geojson = os.path.splitext(input_geojson)[0] + "_3857.json"

# PyInstallerのリソースパス解決用
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ログファイルの設定をさらに修正
try:
    if getattr(sys, 'frozen', False):
        # exe実行時
        log_dir = os.path.join(os.path.dirname(sys.executable), 'logs')
    else:
        # 通常実行時
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    os.makedirs(log_dir, exist_ok=True)
except Exception as e:
    # 失敗した場合は実行ファイルと同じディレクトリを使用
    log_dir = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_dir, exist_ok=True)

# ダイアログでEPSGコードを選択
selected_epsg_code = select_epsg()
print(f"選択されたEPSGコード: {selected_epsg_code}")

# GeoJSONの読み込み
logging.info(f"処理開始: 入力ファイル {input_geojson}")
logging.info("GeoJSONファイルを読み込み中...")
with open(input_geojson, 'r', encoding='utf-8') as f:
    data = json.load(f)
logging.info(f"読み込み完了: {len(data['features'])}件のデータ")

# Shapelyジオメトリに変換
features = []
for feature in data['features']:
    geometry = feature['geometry']
    properties = feature.get('properties', {})
    
    # ジオメトリの変換
    if geometry['type'] == 'Polygon':
        coords = geometry['coordinates']
        geom = Polygon(coords[0]) if coords else None
    elif geometry['type'] == 'Point':
        coords = geometry['coordinates']
        geom = Point(coords) if coords else None
    else:
        geom = None
    
    if geom:
        features.append({'geometry': geom, 'properties': properties})

# GeoDataFrameを作成
gdf = gpd.GeoDataFrame(features)

# 選択したEPSGコードを適用
if gdf.crs is None:
    logging.warning("座標系が設定されていません。EPSG:6677を設定します。")
    gdf = gdf.set_crs(epsg=6677, allow_override=True)

# EPSG:3857に変換
logging.info(f"現在の座標系: {gdf.crs}")
logging.info("EPSG:3857に変換中...")
gdf = gdf.to_crs(epsg=3857)
logging.info(f"変換後の座標系: {gdf.crs}")

# ジオメトリの向きを修正
def fix_polygon_orientation(geometry):
    try:
        if geometry.is_empty:
            return geometry
        elif isinstance(geometry, Polygon):
            return orient(geometry, sign=1.0)
        elif isinstance(geometry, MultiPolygon):
            return MultiPolygon([orient(p, sign=1.0) for p in geometry.geoms])
        return geometry
    except Exception as e:
        logging.error(f"ジオメトリの向き修正でエラー: {str(e)}")
        return geometry

logging.info("ジオメトリの向きを修正中...")
gdf["geometry"] = gdf["geometry"].apply(fix_polygon_orientation)

# 無効なジオメトリの修正
logging.info("無効なジオメトリを修正中...")
gdf["geometry"] = gdf["geometry"].buffer(0)

# 修正済みデータを保存
logging.info(f"ファイルを保存中: {output_geojson}")
output_features = []
for _, row in gdf.iterrows():
    output_features.append({
        "type": "Feature",
        "properties": row["properties"],
        "geometry": mapping(row["geometry"])
    })

output_data = {
    "type": "FeatureCollection",
    "name": os.path.basename(output_geojson),
    "crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG:3857" } },
    "features": output_features
}

with open(output_geojson, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

logging.info("処理が正常に完了しました")
