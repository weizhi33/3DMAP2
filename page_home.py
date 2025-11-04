import streamlit as st

st.set_page_config(page_title="專案首頁")

st.title("🏡 歡迎來到小琉球 3D 地形呈現專案")

st.markdown("""
    ---
    **專案簡介**
    
    * 本應用程式利用**數值地形模型 (DTM / DEM)** 數據，將小琉球的地理高程資料轉化為可互動的 **3D 地形圖**。
    * 使用者可以在地圖上自由拖曳、縮放，直觀地探索島嶼的**高程起伏與地貌特徵**。
""")