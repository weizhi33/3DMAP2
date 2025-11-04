import elevation
import rasterio
import pandas as pd
import numpy as np

# 小琉球 (琉球嶼) 的大致經緯度範圍 (WGS84)
# [西經度, 南緯度, 東經度, 北緯度]
# 這是 'bounds' 格式
XIAOLIUQIU_BOUNDS = [120.35, 22.31, 120.42, 22.37]

# 臨時儲存下載的 GeoTIFF 檔案
OUTPUT_PATH = "xiaoliuqiu_srtm_dem.tif"

# 1. 下載 SRTM 30m DEM 數據
try:
    st.info("正在嘗試下載 SRTM 30m DEM 資料...")
    elevation.clip(
        bounds=XIAOLIUQIU_BOUNDS, 
        output=OUTPUT_PATH, 
        product='SRTM3' # SRTM 3 Arc-second (約 90m) 或 SRTM1 (30m, 需授權)
    )
    st.success(f"DEM 資料已下載到：{OUTPUT_PATH}")

    # 2. 讀取 GeoTIFF 檔案
    with rasterio.open(OUTPUT_PATH) as src:
        # 讀取高程數據 (Z)
        Z_data = src.read(1)
        
        # 獲取 X 和 Y 座標網格
        cols, rows = np.meshgrid(np.arange(src.width), np.arange(src.height))
        
        # 將像素座標轉換為經緯度 (X, Y)
        xs, ys = rasterio.transform.xy(src.transform, rows, cols)
        
        # 將數據轉換為您需要的 Pandas/Plotly 格式
        # 這裡需要將 X, Y, Z 重新結構化，類似於我們前面討論的網格轉換。
        # (這部分會比直接用 CSV 複雜，但可行)
        
        # ... 轉換成 Plotly 需要的 Z_matrix, X_grid, Y_grid ...

        # 接下來接續您 Streamlit/Plotly 的繪圖程式碼
        
except Exception as e:
    st.error(f"自動下載 DEM 失敗。原因：{e}")
    st.warning("請確保您的環境有安裝 `gdal` 函式庫，這是 `elevation` 的依賴項。")