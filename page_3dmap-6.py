import streamlit as st
import plotly.express as px
import pandas as pd

st.title("Plotly 真正的 3D 散点图 (X, Y, Z)")

# --- 1. 载入 Plotly 示例数据 ---
# 筛选出 2007 年的数据
df = px.data.gapminder().query("year == 2007")

# --- 2. 创建真正的 3D 散点图 (px.scatter_3d) ---
fig = px.scatter_3d(
    df,
    x="lifeExp",        # X 轴: 预期寿命
    y="pop",            # Y 轴: 人口
    z="gdpPercap",      # Z 轴: 人均 GDP (作为第三维度)
    color="continent",  # 按洲着色
    hover_name="country", # 鼠标悬停时显示国家
    size="pop",         # 标记点大小按人口
)

# --- 3. 在 Streamlit 中显示 ---
st.plotly_chart(fig, use_container_width=True)