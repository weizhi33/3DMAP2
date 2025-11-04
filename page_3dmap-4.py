import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np # 確保匯入 numpy

st.set_page_config(page_title="Plotly 3D 地形範例")
st.title("⛰️ Mt. Bruno 範例 3D 地形圖")

# --- 1. 載入 DEM 數據 (直接從 Plotly 官方線上 CSV 載入) ---
# 這個 CSV 檔案的格式已經是 Plotly 繪圖所需的 Z 矩陣格式 (每一列都是一個 X/Y 網格的 Z 值)
try:
    z_data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv")
    
    # 轉換成 numpy 陣列
    Z_matrix = z_data.values

    # 顯示數據資訊
    st.info(f"成功載入 Mt. Bruno 數據。高程矩陣大小: {Z_matrix.shape}")

except Exception as e:
    st.error(f"載入 Mt. Bruno 範例數據時發生錯誤: {e}")
    st.warning("請檢查網路連接，或確保 Streamlit Cloud 可以存取該 GitHub 連結。")
    Z_matrix = None


if Z_matrix is not None:
    
    # --- 2. 創建 3D Surface 圖表 ---
    fig = go.Figure(
        data=[go.Surface(
            z=Z_matrix, # 使用已載入的 Z 矩陣
            colorscale="Viridis" # 設定顏色
        )]
    )
    
    # --- 3. 設定 3D 佈局 ---
    fig.update_layout(
        title="Mt. Bruno 3D 表面模型 (範例)",
        width=900,
        height=700,
        scene=dict(
            xaxis_title='網格 (X)', # 由於缺乏實際座標，軸標題使用網格數
            yaxis_title='網格 (Y)',
            zaxis_title='高程 (Z)',
            # 調整比例
            aspectratio=dict(x=1, y=1, z=0.5), 
            aspectmode='manual',
            camera=dict(eye=dict(x=1.8, y=1.8, z=0.8)) # 調整視角
        ),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # --- 4. 顯示在 Streamlit 頁面上 ---
    st.plotly_chart(fig, use_container_width=True)