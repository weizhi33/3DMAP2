import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Plotly 3D 地形範例")
st.title("🏞️ 美國大峽谷 3D 地形圖範例")

# --- 1. 載入 DEM 數據 (Grand Canyon 官方範例數據) ---
# 這個 CSV 檔案與 Mt. Bruno 類似，格式已經是 Plotly 繪圖所需的 Z 矩陣格式
try:
    # Grand Canyon 數據連結
    GRAND_CANYON_URL = "https://raw.githubusercontent.com/plotly/datasets/master/api_docs/grand_canyon_elevation.csv"
    
    # 載入數據
    z_data = pd.read_csv(GRAND_CANYON_URL)
    
    # 轉換成 numpy 陣列
    Z_matrix = z_data.values

    # 顯示數據資訊
    st.info(f"成功載入 Grand Canyon 數據。高程矩陣大小: {Z_matrix.shape}")

except Exception as e:
    st.error(f"載入 Grand Canyon 範例數據時發生錯誤: {e}")
    st.warning("請檢查網路連接。")
    Z_matrix = None


if Z_matrix is not None:
    
    # --- 2. 創建 3D Surface 圖表 ---
    fig = go.Figure(
        data=[go.Surface(
            z=Z_matrix, 
            # 換一個配色方案，讓大峽谷的層次感更強
            colorscale="Sunsetdark", 
            showscale=True,
            # 讓表面有網格線，視覺效果更佳
            contours=dict(
                z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True)
            )
        )]
    )
    
    # --- 3. 設定 3D 佈局 ---
    fig.update_layout(
        title="美國大峽谷 3D 表面模型 (範例)",
        width=900,
        height=700,
        scene=dict(
            xaxis_title='網格 (X)', 
            yaxis_title='網格 (Y)',
            zaxis_title='高程 (Z)',
            # 調整比例，強調峽谷的垂直深度
            aspectratio=dict(x=1, y=1, z=0.7), 
            aspectmode='manual',
            camera=dict(eye=dict(x=1.8, y=-1.5, z=0.8)) # 稍微不同的視角
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # --- 4. 顯示在 Streamlit 頁面上 ---
    st.plotly_chart(fig, use_container_width=True)