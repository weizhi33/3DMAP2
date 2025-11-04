import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np # 用於處理網格數據

# ----------------------------------------------------
# 設定檔案與欄位名稱 (請根據您的實際 CSV 檔案調整！)
# ----------------------------------------------------
# 注意：Streamlit 在部署時會以專案根目錄為基準。
# 如果您的 DTM.csv 就在 app.py 旁邊，路徑會是 'DTM.csv'
# 如果 DTM.csv 在子資料夾 data/ 內，路徑是 'data/DTM.csv'
# 根據您的路徑 /workspaces/1029streamlit3Dwebmaps-sodespace/DTM.csv
# 在 codespace 專案根目錄下，通常就是 'DTM.csv'
DATA_FILE_PATH = 'DTM.csv' 

# 假設您的 CSV 檔案的欄位名稱 (請務必確認這三欄的名稱！)
# DTM 資料通常使用 TWD97 (平面座標)
X_COL_NAME = 'X' 
Y_COL_NAME = 'Y' 
Z_COL_NAME = 'Z' # 高程值

st.set_page_config(
    page_title="小琉球 DTM 3D 模型", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data
def load_and_structure_dtm(file_path):
    """
    讀取 DTM CSV 數據，並將其轉換為 Plotly 繪圖所需的 Z 矩陣。
    這一步驟非常關鍵，將點雲數據轉換為規則的網格 (Grid)。
    """
    try:
        # 1. 讀取數據 (假設 CSV 沒有額外的 Index 欄位)
        df = pd.read_csv(file_path) 
        
        # 2. 篩選：移除缺失值 (若有)
        df = df.dropna(subset=[X_COL_NAME, Y_COL_NAME, Z_COL_NAME])
        
        # 3. 準備 X, Y 唯一值
        # 由於是規則網格，我們按順序取出 X, Y 的唯一座標
        unique_x = sorted(df[X_COL_NAME].unique())
        unique_y = sorted(df[Y_COL_NAME].unique())
        
        nx = len(unique_x)
        ny = len(unique_y)
        
        st.info(f"DTM 數據點數: {len(df)} 點. 網格大小: {nx} (X) x {ny} (Y)")

        # 4. 創建 Z 矩陣
        # 關鍵步驟：使用 pivot_table 將 (X, Y, Z) 轉換為 Z 矩陣
        # 這假設數據是完整的網格，否則需要插補
        
        # 將 Y 軸從最小到最大排序 (Plotly 習慣的矩陣繪圖方式)
        # 如果 Y 值從大到小繪製出來是上下顛倒的，可以嘗試對 unique_y 進行 reverse()
        df_pivot = df.pivot_table(values=Z_COL_NAME, index=Y_COL_NAME, columns=X_COL_NAME)
        
        # 獲取 Z 矩陣 (轉為 numpy 陣列)
        Z_matrix = df_pivot.values
        
        # 重新獲取 X, Y 軸的刻度 (確保與矩陣一致)
        X_grid = df_pivot.columns.tolist()
        Y_grid = df_pivot.index.tolist()
        
        return Z_matrix, X_grid, Y_grid

    except FileNotFoundError:
        st.error(f"錯誤：找不到檔案在路徑 `{file_path}`。請確認檔案名稱和路徑是否正確。")
        return None, None, None
    except KeyError as e:
        st.error(f"錯誤：CSV 檔案中找不到欄位名稱 {e}。請檢查程式碼中的 X_COL_NAME, Y_COL_NAME, Z_COL_NAME 是否與您的檔案標頭一致。")
        return None, None, None
    except Exception as e:
        st.error(f"載入或結構化數據時發生錯誤: {e}")
        return None, None, None

def plot_3d_surface(Z_data, X_grid, Y_grid):
    """使用 Plotly 繪製 3D 表面圖"""
    
    # 創建 3D 表面圖
    fig = go.Figure(data=[
        go.Surface(
            z=Z_data,
            x=X_grid,
            y=Y_grid,
            colorscale='Turbo', # 高對比度的地形配色
            lighting=dict(ambient=0.8, diffuse=0.8, specular=0.2, roughness=0.5, fresnel=0.01),
            contours={
                "z": {"show": True, "start": np.nanmin(Z_data), "end": np.nanmax(Z_data), "size": 5, "color":"white"}
            }
        )
    ])

    # 設定佈局
    fig.update_layout(
        title={
            'text': f'小琉球 DTM 20m 互動式 3D 模型 ({Z_COL_NAME} 單位: 公尺)',
            'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'
        },
        scene=dict(
            xaxis_title=f'{X_COL_NAME} 座標',
            yaxis_title=f'{Y_COL_NAME} 座標',
            zaxis_title=f'{Z_COL_NAME} 高程 (公尺)',
            # 調整 Z 軸的比例，讓地形起伏更明顯
            zaxis_autorange=True,
            aspectratio=dict(x=1, y=1, z=0.5), # 將 Z 軸壓縮，讓島嶼看起來更平坦
            aspectmode='manual',
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.25, y=1.25, z=1.25) # 預設視角
            )
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        height=700
    )
    
    return fig

# ----------------------------------------------------
# Streamlit 主程式
# ----------------------------------------------------

st.title("🏝️ 小琉球 DTM 互動式 3D 地形呈現")
st.markdown("本數據使用 20 公尺網格數值地形模型 (DTM) 繪製，呈現裸露地表的高程起伏。")

# 1. 載入數據
Z_data, X_grid, Y_grid = load_and_structure_dtm(DATA_FILE_PATH)

if Z_data is not None:
    # 2. 繪製圖表
    fig = plot_3d_surface(Z_data, X_grid, Y_grid)
    
    # 3. 顯示在 Streamlit 頁面上
    st.plotly_chart(fig, use_container_width=True)

    # 顯示原始數據資訊 (可選)
    with st.expander("查看數據結構資訊"):
        st.write(f"X 座標範圍：{min(X_grid):.2f} 到 {max(X_grid):.2f}")
        st.write(f"Y 座標範圍：{min(Y_grid):.2f} 到 {max(Y_grid):.2f}")
        st.write(f"高程 (Z) 範圍：{np.nanmin(Z_data):.2f} 公尺 到 {np.nanmax(Z_data):.2f} 公尺")