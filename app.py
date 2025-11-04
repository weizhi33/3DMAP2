import streamlit as st

# 1. 使用 st.Page() 定義所有頁面 (暫時使用純英文標題來排除中文字元問題)
pages = [
    st.Page("page_home.py", title="Home Page", icon="🏠"),
    st.Page("page_3dmap-1.py", title="Pydeck 3D Map", icon="🌏"),
    st.Page("page_3dmap-2.py", title="Plotly 小琉球失敗", icon="ℹ️"),
    st.Page("page_3dmap-3.py", title="Plotly 小琉球失敗", icon="ℹ️"),
    st.Page("page_3dmap-4.py", title="Plotly 大峽谷失敗", icon="ℹ️"),
    st.Page("page_3dmap-5.py", title="Plotly MT山 成功", icon="ℹ️"),
    st.Page("page_3dmap-6.py", title="Plotly 3D 散點圖", icon="ℹ️"),
    st.Page("page_3dmap-7.py", title="Plotly 人均 GDP 與預期壽命分佈 成功", icon="ℹ️")
]

# 2. 使用 st.navigation() 建立導覽
with st.sidebar:
    st.title("About Me")
    selected_page = st.navigation(pages)


# 3. 執行被選擇的頁面
selected_page.run() # 這是現在的第 18 行