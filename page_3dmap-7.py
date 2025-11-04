import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Plotly 地理地图（正射投影 - 地球仪效果）")

# --- 1. 载入 Plotly 示例数据 ---
df = px.data.gapminder().query("year == 2007")

# --- 2. 创建地理散点图 (px.scatter_geo) ---
fig = px.scatter_geo(
    df,
    locations="iso_alpha",  # 使用国家三字母代码来定位
    color="continent",      # 按洲着色
    hover_name="country",   # 鼠标悬停时显示国家
    size="pop",             # 标记点大小按人口
    projection="orthographic" # 使用正射投影，呈现出 3D-like 的地球仪外观
)

# --- 3. 在 Streamlit 中显示 ---
st.plotly_chart(fig, use_container_width=True)