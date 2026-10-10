import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8')

# 1. 标题： 的《加州住房数据（1990 年）》
st.title('[易千雅] 的《加州住房数据（1990 年）》')

# 读取数据
@st.cache_data
def load_data():
    return pd.read_csv('housing.csv')

df = load_data()

# 2. 一个名为“最低房屋中位价”的滑块，取值范围为 0 到 500001，默认值为 200000
price_filter = st.slider(
    '最低房屋中位价',
    min_value=0,
    max_value=500001,
    value=200000
)

# 3. 副标题：在侧边栏查看更多筛选条件：
st.subheader('在侧边栏查看更多筛选条件：')

# 4. 侧边栏中名为“选择位置类型”的多选控件，用于筛选 ocean_proximity，默认全选
ocean_types = list(df['ocean_proximity'].dropna().unique())
selected_ocean_types = st.sidebar.multiselect(
    '选择位置类型',
    options=ocean_types,
    default=ocean_types
)

# 5. 侧边栏中名为“选择收入水平”的单选按钮组件 (st.radio)
income_level = st.sidebar.radio(
    '选择收入水平',
    ('低', '中等', '高')
)

# --- 筛选逻辑 ---
# 过滤 median_house_value
filtered_df = df[df['median_house_value'] >= price_filter]

# 过滤 ocean_proximity
filtered_df = filtered_df[filtered_df['ocean_proximity'].isin(selected_ocean_types)]

# 使用 if 语句根据收入水平过滤
if income_level == '低':
    filtered_df = filtered_df[filtered_df['median_income'] <= 2.5]
elif income_level == '中等':
    filtered_df = filtered_df[(filtered_df['median_income'] > 2.5) & (filtered_df['median_income'] < 4.5)]
elif income_level == '高':
    filtered_df = filtered_df[filtered_df['median_income'] >= 4.5]

# 6. 已筛选区域的地图
st.map(filtered_df[['latitude', 'longitude']])

# 7. 地图下方是 median_house_value 经过筛选的区域的直方图，分为 30 个区间
fig, ax = plt.subplots(figsize=(10, 5))
filtered_df['median_house_value'].plot.hist(
    bins=30, 
    ax=ax, 
    edgecolor='black',