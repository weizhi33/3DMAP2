import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotly 3D 地形範例")
st.title("🏞️ 美國大峽谷 3D 地形圖範例")

# --- 1. 載入 DEM 數據 (Grand Canyon 官方範例數據 - 使用新連結) ---
try:
    # 修正後的 Grand Canyon 數據連結 (指向另一個 Plotly 數據集)
    # 這個連結指向的數據與 Grand Canyon 數據格式相似，可以成功繪製 3D 地形。
    GRAND_CANYON_URL = "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt-bruno-elevation.csv" # 暫時使用這個穩定的，並修改標題
    
    # 載入數據
    z_data = pd.read_csv(GRAND_CANYON_URL, header=None) # 注意：這個連結可能是無標頭的，先嘗試無標頭讀取
    
    # 轉換成 numpy 陣列
    Z_matrix = z_data.values

    # 顯示數據資訊
    st.info(f"成功載入範例 DEM 數據。高程矩陣大小: {Z_matrix.shape}")

except Exception as e:
    st.error(f"載入範例數據時發生錯誤: {e}")
    st.warning("請檢查網路連接。")
    Z_matrix = None


if Z_matrix is not None:
    
    # --- 2. 創建 3D Surface 圖表 ---
    fig = go.Figure(
        data=[go.Surface(
            z=Z_matrix, 
            colorscale="Sunsetdark", 
            showscale=True,
            contours=dict(
                z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True)
            )
        )]
    )
    
    # --- 3. 設定 3D 佈局 ---
    fig.update_layout(
        title="替換範例：Plotly 3D 表面模型", # 更改標題以反映我們使用了替代數據
        width=900,
        height=700,
        scene=dict(
            xaxis_title='網格 (X)', 
            yaxis_title='網格 (Y)',
            zaxis_title='高程 (Z)',
            aspectratio=dict(x=1, y=1, z=0.7), 
            aspectmode='manual',
            camera=dict(eye=dict(x=1.8, y=-1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # --- 4. 顯示在 Streamlit 頁面上 ---
    st.plotly_chart(fig, use_container_width=True)