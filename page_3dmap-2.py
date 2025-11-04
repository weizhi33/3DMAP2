import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------------------
# 程式設定
# ----------------------------------------------------
st.set_page_config(
    page_title="小琉球 SRTM DEM 3D 模型", 
    layout="wide",
)

# 小琉球 (琉球嶼) 的大致經緯度範圍 (WGS84)
# [西經度, 南緯度, 東經度, 北緯度]
XIAOLIUQIU_BOUNDS = [120.35, 22.31, 120.42, 22.37]
OUTPUT_PATH = "xiaoliuqiu_srtm_dem.tif"

@st.cache_data
def download_and_process_dem(bounds, output_path):
    """下載 SRTM DEM 並將其轉換為 Plotly 網格數據"""
    try:
        st.info("正在嘗試下載 SRTM 90m DEM 資料 (SRTM3)...")
        
        # 1. 下載 SRTM 3 Arc-second (~90m) DEM 數據
        # 注意：使用 SRTM3 數據，因為 SRTM1 (30m) 經常需要 Earthdata 授權才能下載。
        import elevation
        elevation.clip(
            bounds=bounds, 
            output=output_path, 
            product='SRTM3'
        )
        st.success(f"DEM 資料已下載到：{output_path}")

        # 2. 讀取 GeoTIFF 檔案並轉換為網格數據
        import rasterio
        with rasterio.open(output_path) as src:
            Z_data = src.read(1) # 讀取高程數據 (Z)
            
            # 替換無效值 (NoDataValue) 為 NaN
            if src.nodata is not None:
                Z_data[Z_data == src.nodata] = np.nan

            # 創建 X 和 Y 座標網格 (這就是 Plotly 需要的 X_grid, Y_grid)
            # x_coords: 經度, y_coords: 緯度
            x_coords = np.linspace(src.bounds.left, src.bounds.right, src.width)
            y_coords = np.linspace(src.bounds.bottom, src.bounds.top, src.height)
            
            # 因為 Plotly 的 y 軸是從下到上，但 GeoTIFF 數據通常是從上到下，需要反轉 Z 數據和 Y 座標
            Z_matrix = Z_data[::-1]
            Y_grid = y_coords[::-1] 
            X_grid = x_coords

            return Z_matrix, X_grid, Y_grid

    except ImportError:
        st.error("請確保您已安裝 'elevation' 和 'rasterio' 函式庫。")
        return None, None, None
    except Exception as e:
        st.error(f"自動下載或處理 DEM 失敗。原因：{e}")
        st.warning("如果錯誤與 'gdal' 相關，請確保部署環境中有安裝 GDAL 依賴。")
        return None, None, None

def plot_3d_surface(Z_data, X_grid, Y_grid):
    """使用 Plotly 繪製 3D 表面圖"""
    
    fig = go.Figure(data=[
        go.Surface(
            z=Z_data,
            x=X_grid,
            y=Y_grid,
            colorscale='Topo', # 地形配色方案
            # 設定等高線
            contours={
                "z": {"show": True, "start": np.nanmin(Z_data), "end": np.nanmax(Z_data), "size": 10, "color":"white"}
            }
        )
    ])

    fig.update_layout(
        title='小琉球 SRTM DEM 3D 地形呈現',
        scene=dict(
            xaxis_title='經度 (X)',
            yaxis_title='緯度 (Y)',
            zaxis_title='高程 (Z) 公尺',
            # 調整 Z 軸的比例，讓地形起伏更明顯
            aspectratio=dict(x=1, y=1.2, z=0.5), 
            aspectmode='manual',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.25, y=1.25, z=1.25)
            )
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=700
    )
    
    return fig

# ----------------------------------------------------
# Streamlit 主程式
# ----------------------------------------------------

st.title("🏝️ 小琉球 DEM 互動式 3D 模型 (SRTM 90m)")

# 1. 載入數據 (如果已經下載過，st.cache_data 會加速)
Z_data, X_grid, Y_grid = download_and_process_dem(XIAOLIUQIU_BOUNDS, OUTPUT_PATH)

if Z_data is not None:
    # 2. 繪製圖表
    fig = plot_3d_surface(Z_data, X_grid, Y_grid)
    
    # 3. 顯示在 Streamlit 頁面上
    st.plotly_chart(fig, use_container_width=True)

    # 顯示數據資訊
    with st.expander("數據資訊"):
        st.write(f"高程 (Z) 範圍：{np.nanmin(Z_data):.2f} 公尺 到 {np.nanmax(Z_data):.2f} 公尺")