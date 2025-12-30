# encoding: utf-8

import pandas as pd
import numpy as np

"""
Python 数据科学的基石
Pandas 是 Python 最核心的数据处理与分析库，为处理表格数据（如 Excel 表格、SQL 数据库）和时间序列数据提供了强大、灵活且高性能的数据结构。



"""

# 1. 核心概念与数据结构
# 1.1. DataFrame（二维表格）
# 创建 DataFrame
data = {
    '姓名': ['张三', '李四', '王五', '赵六'],
    '年龄': [25, 30, 35, 28],
    '城市': ['北京', '上海', '广州', '深圳'],
    '薪资': [15000, 22000, 18000, 25000]
}

df = pd.DataFrame(data)
print(df)
"""
   姓名  年龄  城市     薪资
0  张三  25  北京  15000
1  李四  30  上海  22000
2  王五  35  广州  18000
3  赵六  28  深圳  25000
"""

# DataFrame 基本信息
print(f"形状: {df.shape}")        # (4, 4) - 4行4列
print(f"列名: {df.columns.tolist()}")
print(f"数据类型:\n{df.dtypes}")

# 1.2. Series（一维序列）
# 创建 Series
ages = pd.Series([25, 30, 35, 28], name='年龄')
print(ages)
"""
0    25
1    30
2    35
3    28
Name: 年龄, dtype: int64
"""

# 从 DataFrame 获取 Series
salaries = df['薪资']
print(type(salaries))  # <class 'pandas.core.series.Series'>


# 2. 数据读取与写入
# 读取各种格式的数据
df_csv = pd.read_csv('data.csv')          # CSV 文件
df_excel = pd.read_excel('data.xlsx')     # Excel 文件
df_json = pd.read_json('data.json')       # JSON 文件
df_sql = pd.read_sql('SELECT * FROM table', connection)  # SQL 数据库

# 写入数据
df.to_csv('output.csv', index=False)      # 写入 CSV
df.to_excel('output.xlsx', index=False)   # 写入 Excel
df.to_json('output.json', orient='records')  # 写入 JSON
df.to_sql('table_name', connection, if_exists='replace')  # 写入 SQL

# 常用读取参数示例
df = pd.read_csv('data.csv',
                 encoding='utf-8',        # 编码格式
                 sep=',',                 # 分隔符
                 header=0,                # 标题行
                 skiprows=[0, 2],         # 跳过指定行
                 nrows=1000,              # 读取前1000行
                 parse_dates=['日期列'])   # 解析日期列


# 3. 数据查看与探索
# 查看数据
print(df.head())          # 前5行
print(df.tail(3))         # 后3行
print(df.sample(5))       # 随机5行

# 数据信息
df.info()                 # 数据类型、内存使用等
print(df.describe())      # 数值列统计摘要

# 统计信息
print(df['薪资'].mean())   # 平均值
print(df['薪资'].median()) # 中位数
print(df['薪资'].std())    # 标准差
print(df['薪资'].min())    # 最小值
print(df['薪资'].max())    # 最大值
print(df['薪资'].quantile(0.25))  # 25%分位数

# 唯一值和计数
print(df['城市'].unique())    # 唯一城市
print(df['城市'].value_counts())  # 各城市计数
print(df['城市'].nunique())   # 唯一值数量


# 4. 数据筛选与选择
# 列选择
print(df['姓名'])                    # 单列（Series）
print(df[['姓名', '薪资']])           # 多列（DataFrame）
print(df.loc[:, '姓名':'城市'])       # 按标签选择列范围
print(df.iloc[:, 0:2])              # 按位置选择列

# 行选择
print(df.loc[0])                    # 按标签选择行
print(df.loc[0:2])                  # 按标签选择行范围
print(df.iloc[0])                   # 按位置选择行
print(df.iloc[0:3])                 # 按位置选择行范围

# 条件筛选
high_salary = df[df['薪资'] > 20000]          # 薪资 > 20000
beijing_young = df[(df['城市'] == '北京') & (df['年龄'] < 30)]  # 北京且年龄<30
shanghai_or_guangzhou = df[df['城市'].isin(['上海', '广州'])]  # 上海或广州

# 查询方法
result = df.query('薪资 > 20000 and 年龄 < 35')
result = df.query('城市 in ["北京", "上海"]')


# 5. 数据处理与清洗
# 处理缺失值
df_with_nulls = pd.DataFrame({
    'A': [1, 2, np.nan, 4],
    'B': [5, np.nan, np.nan, 8],
    'C': [10, 20, 30, 40]
})

print(df_with_nulls.isnull())       # 检查缺失值
print(df_with_nulls.isnull().sum()) # 每列缺失值数量

# 删除缺失值
df_dropped = df_with_nulls.dropna()            # 删除任何包含NaN的行
df_dropped_col = df_with_nulls.dropna(axis=1)  # 删除任何包含NaN的列
df_dropped_thresh = df_with_nulls.dropna(thresh=2)  # 至少2个非NaN值

# 填充缺失值
df_filled_zero = df_with_nulls.fillna(0)           # 用0填充
df_filled_mean = df_with_nulls.fillna(df_with_nulls.mean())  # 用均值填充
df_filled_ffill = df_with_nulls.fillna(method='ffill')  # 用前一个值填充
df_filled_bfill = df_with_nulls.fillna(method='bfill')  # 用后一个值填充

# 处理重复值
df_with_duplicates = pd.DataFrame({
    'A': [1, 2, 2, 3, 4, 4, 4],
    'B': ['x', 'y', 'y', 'z', 'x', 'x', 'x']
})

print(df_with_duplicates.duplicated())        # 标记重复行
df_no_duplicates = df_with_duplicates.drop_duplicates()  # 删除重复行
df_no_duplicates_subset = df_with_duplicates.drop_duplicates(subset=['A'])  # 基于A列去重

# 数据类型转换
df['年龄'] = df['年龄'].astype('float32')  # 转换为float32
df['薪资'] = pd.to_numeric(df['薪资'], errors='coerce')  # 安全转换为数值

# 重命名列
df_renamed = df.rename(columns={'姓名': 'name', '年龄': 'age'})
df_renamed.columns = ['name', 'age', 'city', 'salary']  # 批量重命名

# 重置索引
df_reset = df.reset_index(drop=True)  # 重置为连续索引，不保留原索引
df_reset_keep = df.reset_index()      # 重置索引，原索引变为列


# 6. 数据转换
# 添加新列
df['年薪'] = df['薪资'] * 12
df['薪资等级'] = np.where(df['薪资'] > 20000, '高', '低')
df['年龄组'] = pd.cut(df['年龄'],
                    bins=[20, 30, 40, 50],
                    labels=['青年', '中年', '中老年'])

# 应用函数
def categorize_salary(salary):
    if salary < 18000:
        return '初级'
    elif salary < 25000:
        return '中级'
    else:
        return '高级'

df['薪资分类'] = df['薪资'].apply(categorize_salary)
df['姓名长度'] = df['姓名'].apply(len)
df['薪资平方'] = df['薪资'].apply(lambda x: x ** 2)

# 向量化操作（更快）
df['薪资加10%'] = df['薪资'] * 1.1
df['年龄平方'] = df['年龄'] ** 2

# 数据透视表
pivot = df.pivot_table(values='薪资',
                      index='城市',
                      columns='薪资等级',
                      aggfunc='mean',
                      fill_value=0)
print(pivot)

# 分组操作
grouped = df.groupby('城市')
print(grouped['薪资'].mean())        # 每个城市的平均薪资
print(grouped['年龄'].agg(['mean', 'min', 'max', 'count']))  # 多个聚合
print(grouped.agg({'薪资': 'mean', '年龄': ['min', 'max']}))  # 不同列不同聚合

# 分组后应用复杂函数
def top_n_salaries(group, n=2):
    return group.nlargest(n, '薪资')

top_salaries = df.groupby('城市', group_keys=False).apply(top_n_salaries, n=1)
print(top_salaries)


# 7. 数据合并与连接
# 创建示例数据
df1 = pd.DataFrame({
    'ID': [1, 2, 3, 4],
    '姓名': ['张三', '李四', '王五', '赵六'],
    '部门': ['技术', '市场', '技术', '人事']
})

df2 = pd.DataFrame({
    'ID': [1, 2, 3, 5],
    '薪资': [15000, 22000, 18000, 20000],
    '入职年份': [2019, 2020, 2018, 2021]
})

# 合并（merge）- 类似 SQL JOIN
inner_join = pd.merge(df1, df2, on='ID', how='inner')      # 内连接
left_join = pd.merge(df1, df2, on='ID', how='left')        # 左连接
right_join = pd.merge(df1, df2, on='ID', how='right')      # 右连接
outer_join = pd.merge(df1, df2, on='ID', how='outer')      # 全外连接

# 指定不同列名进行合并
df3 = pd.DataFrame({'员工ID': [1, 2, 3], '奖金': [5000, 3000, 4000]})
merged = pd.merge(df1, df3, left_on='ID', right_on='员工ID')

# 拼接（concat）
df_a = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df_b = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
concatenated = pd.concat([df_a, df_b], ignore_index=True)  # 垂直拼接
concatenated_col = pd.concat([df_a, df_b], axis=1)         # 水平拼接

# 追加（append）- 已弃用，推荐使用 concat
# appended = df_a.append(df_b, ignore_index=True)