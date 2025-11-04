import streamlit as st
import plotly.express as px
import pandas as pd

st.title("🗺️ Plotly 地理地圖：人均 GDP 與預期壽命分佈")

# --- 1. 載入 Plotly 示例資料 ---
# 篩選出 2007 年的資料
df = px.data.gapminder().query("year == 2007")

# --- 2. 創建地理散點圖 (px.scatter_geo) 並修改資料欄位 ---
fig = px.scatter_geo(
    df,
    locations="iso_alpha",  # 使用國家三字母代碼來定位
    color="lifeExp",        # **【修改點】** 顏色按「預期壽命」分佈 (連續色階)
    hover_name="country",   # 鼠標懸停時顯示國家名稱
    size="gdpPercap",       # **【修改點】** 圓圈大小按「人均 GDP」顯示
    projection="orthographic", # 使用正射投影，呈現出 3D-like 的地球儀外觀
    title="全球國家 人均 GDP 與預期壽命分佈 (2007)"
)

# --- 3. 在 Streamlit 中顯示 ---
st.plotly_chart(fig, use_container_width=True)