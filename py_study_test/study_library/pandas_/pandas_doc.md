# Pandas 核心 API 学习指南

> 🐼 Python 数据分析必备库 - 从入门到精通

---

## 📚 目录

1. [基础概念](#基础概念)
2. [核心数据结构](#核心数据结构)
3. [数据读写操作](#数据读写操作)
4. [数据查看与探索](#数据查看与探索)
5. [数据筛选与选择](#数据筛选与选择)
6. [数据处理与清洗](#数据处理与清洗)
7. [数据转换与计算](#数据转换与计算)
8. [数据合并与连接](#数据合并与连接)
9. [分组与聚合](#分组与聚合)
10. [时间序列处理](#时间序列处理)
11. [数据可视化](#数据可视化)
12. [最佳实践](#最佳实践)

---

## 基础概念

### 什么是 Pandas？

Pandas 是 Python 中最流行的数据分析库，提供了高性能、易用的数据结构和数据分析工具。

### 主要特点

- 🚀 高性能数据操作
- 📊 强大的数据清洗能力
- 🔗 灵活的数据合并功能
- 📈 丰富的统计分析方法
- 💾 多种数据格式支持

---

## 核心数据结构

### DataFrame（数据框）

二维表格数据结构，类似 Excel 表格或数据库表

```python
import pandas as pd
import numpy as np

# 创建 DataFrame
data = {
    '姓名': ['张三', '李四', '王五'],
    '年龄': [25, 30, 35],
    '薪资': [15000, 22000, 18000]
}
df = pd.DataFrame(data)
print(df)
```

### Series（序列）

一维数组结构，DataFrame 的单列数据

```python
# 创建 Series
ages = pd.Series([25, 30, 35], name='年龄')
print(ages)
```

### 基本属性

```python
# 基本信息
print(f"形状: {df.shape}")          # (行数, 列数)
print(f"列名: {df.columns.tolist()}")
print(f"索引: {df.index.tolist()}")
print(f"数据类型:\n{df.dtypes}")
```

---

## 数据读写操作

### 读取数据

#### CSV 文件

```python
# 基础读取
df = pd.read_csv('data.csv')

# 带参数读取
df = pd.read_csv('data.csv',
                 encoding='utf-8',      # 编码格式
                 sep=',',               # 分隔符
                 header=0,              # 标题行
                 index_col=0,           # 索引列
                 usecols=['A', 'B'],    # 指定列
                 skiprows=2,            # 跳过行数
                 nrows=1000,            # 读取行数
                 na_values=['N/A', 'NULL'],  # 缺失值标识
                 parse_dates=['date'],  # 解析日期列
                 dtype={'col': 'str'})  # 指定数据类型
```

#### Excel 文件

```python
df = pd.read_excel('data.xlsx', 
                   sheet_name='Sheet1',
                   header=0)
```

#### JSON 文件

```python
df = pd.read_json('data.json')
```

#### SQL 数据库

```python
import sqlite3
conn = sqlite3.connect('database.db')
df = pd.read_sql('SELECT * FROM table_name', conn)
```

### 写入数据

#### 保存为 CSV

```python
df.to_csv('output.csv', 
          index=False,           # 不保存索引
          encoding='utf-8')
```

#### 保存为 Excel

```python
df.to_excel('output.xlsx', 
            index=False,
            sheet_name='数据')
```

#### 保存为 JSON

```python
df.to_json('output.json', 
           orient='records',      # 记录格式
           force_ascii=False)     # 支持中文
```

---

## 数据查看与探索

### 基本查看方法

```python
# 查看前几行
print(df.head())        # 默认前5行
print(df.head(10))      # 前10行

# 查看后几行
print(df.tail())        # 默认后5行
print(df.tail(3))       # 后3行

# 随机抽样
print(df.sample(5))     # 随机5行
print(df.sample(frac=0.1))  # 随机10%数据
```

### 数据信息

```python
# 基本信息
df.info()

# 统计摘要（数值列）
print(df.describe())

# 统计摘要（分类列）
print(df.describe(include=['object']))

# 内存使用情况
print(df.memory_usage(deep=True))
```

### 统计分析

```python
# 基础统计
print(f"均值: {df['薪资'].mean()}")
print(f"中位数: {df['薪资'].median()}")
print(f"标准差: {df['薪资'].std()}")
print(f"最小值: {df['薪资'].min()}")
print(f"最大值: {df['薪资'].max()}")

# 分位数
print(df['薪资'].quantile([0.25, 0.5, 0.75]))

# 唯一值统计
print(f"唯一值: {df['部门'].unique()}")
print(f"值计数:\n{df['部门'].value_counts()}")
print(f"唯一值数量: {df['部门'].nunique()}")
```

---

## 数据筛选与选择

### 列选择

```python
# 单列选择（返回 Series）
print(df['姓名'])

# 多列选择（返回 DataFrame）
print(df[['姓名', '薪资']])

# 使用属性方式访问（仅限合法列名）
print(df.姓名)  # 不推荐，容易出错
```

### 行选择

#### 基于标签（loc）

```python
# 选择单行
print(df.loc[0])

# 选择多行
print(df.loc[0:2])          # 包含索引2
print(df.loc[[0, 2, 4]])    # 选择特定行

# 选择行列组合
print(df.loc[0:2, '姓名':'薪资'])  # 行范围 + 列范围
print(df.loc[:, ['姓名', '薪资']]) # 所有行 + 特定列
```

#### 基于位置（iloc）

```python
# 选择单行
print(df.iloc[0])

# 选择多行
print(df.iloc[0:3])         # 不包含位置3
print(df.iloc[[0, 2, 4]])

# 选择行列组合
print(df.iloc[0:3, 0:2])    # 位置范围
print(df.iloc[:, [0, 2]])   # 所有行 + 特定列位置
```

### 条件筛选

```python
# 基础条件筛选
high_salary = df[df['薪资'] > 20000]
print(high_salary)

# 复合条件（AND）
result = df[(df['薪资'] > 18000) & (df['年龄'] < 35)]
print(result)

# 复合条件（OR）
result = df[(df['部门'] == '技术部') | (df['薪资'] > 20000)]
print(result)

# 使用 isin 方法
departments = df[df['部门'].isin(['技术部', '市场部'])]
print(departments)

# 使用 query 方法（更直观）
result = df.query('薪资 > 18000 and 年龄 < 35')
result = df.query('部门 in ["技术部", "市场部"]')
print(result)
```

---

## 数据处理与清洗

### 缺失值处理

#### 检查缺失值

```python
# 检查缺失值
print(df.isnull())

# 统计每列缺失值数量
print(df.isnull().sum())

# 统计每行缺失值数量
print(df.isnull().sum(axis=1))
```

#### 删除缺失值

```python
# 删除包含缺失值的行
df_cleaned = df.dropna()

# 删除包含缺失值的列
df_cleaned = df.dropna(axis=1)

# 设置阈值（至少需要3个非空值）
df_cleaned = df.dropna(thresh=3)

# 基于特定列删除
df_cleaned = df.dropna(subset=['姓名', '薪资'])
```

#### 填充缺失值

```python
# 用固定值填充
df_filled = df.fillna(0)
df_filled = df.fillna('未知')

# 用统计值填充
df_filled = df.fillna(df.mean())        # 均值
df_filled = df.fillna(df.median())      # 中位数

# 前向填充
df_filled = df.ffill()  # 或 df.fillna(method='ffill')

# 后向填充
df_filled = df.bfill()  # 或 df.fillna(method='bfill')

# 用字典指定不同列的填充值
fill_values = {'年龄': df['年龄'].mean(), '薪资': 0}
df_filled = df.fillna(fill_values)
```

### 重复值处理

```python
# 检查重复行
print(df.duplicated())

# 检查基于特定列的重复
print(df.duplicated(subset=['姓名']))

# 删除重复行（保留第一个）
df_unique = df.drop_duplicates()

# 删除重复行（保留最后一个）
df_unique = df.drop_duplicates(keep='last')

# 基于特定列去重
df_unique = df.drop_duplicates(subset=['姓名'])
```

### 数据类型转换

```python
# 转换为指定类型
df['年龄'] = df['年龄'].astype('int32')
df['薪资'] = df['薪资'].astype('float64')

# 安全转换（错误转为 NaN）
df['数字列'] = pd.to_numeric(df['混合列'], errors='coerce')

# 转换为分类类型（节省内存）
df['部门'] = df['部门'].astype('category')

# 转换为日期类型
df['日期'] = pd.to_datetime(df['日期列'])
```

### 列重命名

```python
# 重命名单个或多个列
df_renamed = df.rename(columns={
    '姓名': 'name',
    '年龄': 'age',
    '薪资': 'salary'
})

# 批量重命名所有列
df.columns = ['name', 'age', 'department', 'salary']

# 使用函数重命名
df_renamed = df.rename(columns=str.upper)  # 全部转大写
```

### 索引操作

```python
# 重置索引
df_reset = df.reset_index(drop=True)    # 丢弃原索引
df_reset = df.reset_index()             # 原索引变列

# 设置新索引
df_indexed = df.set_index('姓名')

# 多级索引
df_multiindex = df.set_index(['部门', '姓名'])
```

---

## 数据转换与计算

### 添加新列

```python
# 基础运算
df['年薪'] = df['月薪'] * 12
df['总收入'] = df['基本工资'] + df['奖金']

# 条件赋值
df['薪资等级'] = np.where(df['薪资'] >= 20000, '高级',
                     np.where(df['薪资'] >= 15000, '中级', '初级'))

# 使用 cut 进行分箱
df['年龄组'] = pd.cut(df['年龄'],
                     bins=[0, 25, 35, 50],
                     labels=['青年', '中年', '中老年'])

# 使用 qcut 按分位数分箱
df['薪资分位'] = pd.qcut(df['薪资'], q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
```

### 函数应用

#### apply 方法

```python
# 对 Series 应用函数
def categorize_age(age):
    if age < 30:
        return '青年'
    elif age < 40:
        return '中年'
    else:
        return '中老年'

df['年龄分类'] = df['年龄'].apply(categorize_age)

# 对 DataFrame 应用函数（逐行）
def process_row(row):
    return row['薪资'] * row['绩效系数']

df['调整后薪资'] = df.apply(process_row, axis=1)

# 使用 lambda 函数
df['姓名长度'] = df['姓名'].apply(lambda x: len(x))
df['薪资倍数'] = df['薪资'].apply(lambda x: x / 1000)
```

#### map 方法（仅适用于 Series）

```python
# 映射字典
dept_mapping = {'技术部': 'Tech', '市场部': 'Marketing', '人事部': 'HR'}
df['部门英文'] = df['部门'].map(dept_mapping)

# 映射函数
df['薪资评级'] = df['薪资'].map(lambda x: 'High' if x > 20000 else 'Low')
```

#### 向量化操作（推荐）

```python
# 比 apply 更快的向量化操作
df['新薪资'] = df['薪资'] * 1.1 + 1000
df['薪资差'] = df['实际薪资'] - df['预期薪资']
```

---

## 数据合并与连接

### merge 连接（类似 SQL JOIN）

#### 基础连接

```python
# 内连接（默认）
result = pd.merge(df1, df2, on='共同列')

# 左连接
result = pd.merge(df1, df2, on='共同列', how='left')

# 右连接
result = pd.merge(df1, df2, on='共同列', how='right')

# 外连接
result = pd.merge(df1, df2, on='共同列', how='outer')
```

#### 复杂连接场景

```python
# 基于不同列名连接
result = pd.merge(df1, df2, left_on='员工ID', right_on='ID')

# 多列连接
result = pd.merge(df1, df2, on=['部门', '年份'])

# 指定后缀处理重复列名
result = pd.merge(df1, df2, on='ID', suffixes=('_left', '_right'))
```

### concat 拼接

#### 垂直拼接（增加行）

```python
# 基础垂直拼接
result = pd.concat([df1, df2, df3], ignore_index=True)

# 保持原索引
result = pd.concat([df1, df2])
```

#### 水平拼接（增加列）

```python
# 水平拼接
result = pd.concat([df1, df2], axis=1)

# 处理索引不匹配
result = pd.concat([df1, df2], axis=1, join='inner')  # 内连接
result = pd.concat([df1, df2], axis=1, join='outer')  # 外连接
```

### append 方法（已弃用）

```python
# 旧方法（不推荐）
# result = df1.append(df2, ignore_index=True)

# 新方法（推荐使用 concat）
result = pd.concat([df1, df2], ignore_index=True)
```

---

## 分组与聚合

### 基础分组

```python
# 单列分组
grouped = df.groupby('部门')

# 查看分组信息
print(grouped.groups)  # 显示各组的索引
print(grouped.size())  # 每组的数量

# 多列分组
grouped = df.groupby(['部门', '年龄组'])
```

### 聚合操作

```python
# 单一聚合函数
salary_avg = df.groupby('部门')['薪资'].mean()
salary_stats = df.groupby('部门')['薪资'].agg(['mean', 'min', 'max', 'count'])

# 多列不同聚合
result = df.groupby('部门').agg({
    '薪资': ['mean', 'sum'],
    '年龄': ['min', 'max'],
    '姓名': 'count'
})

# 重命名聚合列
result = df.groupby('部门').agg({
    '薪资': [('平均薪资', 'mean'), ('薪资总和', 'sum')],
    '年龄': [('最小年龄', 'min'), ('最大年龄', 'max')]
})
```

### 自定义聚合函数

```python
# 定义自定义函数
def salary_range(series):
    return series.max() - series.min()

def top_performers(series):
    return series.nlargest(3).tolist()

# 应用自定义聚合
result = df.groupby('部门').agg({
    '薪资': ['mean', salary_range],
    '绩效评分': top_performers
})
```

### 分组后应用（apply）

```python
# 对每组应用复杂函数
def get_top_earners(group, n=2):
    return group.nlargest(n, '薪资')

# 应用函数
top_earners = df.groupby('部门', group_keys=False).apply(get_top_earners, n=1)

# 变换操作（transform）
df['部门平均薪资'] = df.groupby('部门')['薪资'].transform('mean')
df['薪资排名'] = df.groupby('部门')['薪资'].rank(ascending=False)
```

### 数据透视表

```python
# 基础透视表
pivot = df.pivot_table(
    values='薪资',              # 数值列
    index='部门',               # 行索引
    columns='薪资等级',         # 列索引
    aggfunc='mean',             # 聚合函数
    fill_value=0               # 填充空值
)

# 多级透视表
pivot = df.pivot_table(
    values=['薪资', '年龄'],
    index=['部门', '年龄组'],
    columns='薪资等级',
    aggfunc={'薪资': 'mean', '年龄': 'max'}
)

# 添加总计
pivot = df.pivot_table(
    values='薪资',
    index='部门',
    columns='薪资等级',
    aggfunc='mean',
    margins=True,              # 添加总计行/列
    margins_name='总计'         # 总计标签
)
```

### 交叉表

```python
# 基础交叉表
crosstab = pd.crosstab(df['部门'], df['薪资等级'])

# 带汇总统计的交叉表
crosstab = pd.crosstab(
    df['部门'], 
    df['薪资等级'],
    values=df['薪资'],         # 数值列
    aggfunc='mean',            # 聚合函数
    normalize='index'          # 百分比（按行）
)
```

---

## 时间序列处理

### 创建时间序列

```python
# 日期范围
dates = pd.date_range('2023-01-01', periods=12, freq='ME')  # 月末
dates = pd.date_range('2023-01-01', periods=365, freq='D')   # 每天
dates = pd.date_range('2023-01-01', '2023-12-31', freq='W')  # 每周

# 转换为日期时间
df['日期'] = pd.to_datetime(df['日期列'])
```

### 时间序列属性.

```python
# 提取时间组件
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day
df['星期'] = df['日期'].dt.dayofweek  # 0=周一, 6=周日
df['是否周末'] = df['日期'].dt.weekday >= 5

# 时间周期
df['季度'] = df['日期'].dt.quarter
df['月份名称'] = df['日期'].dt.month_name()
df['星期名称'] = df['日期'].dt.day_name()
```

### 时间重采样

```python
# 设置时间为索引
df_ts = df.set_index('日期')

# 按月重采样
monthly = df_ts.resample('ME').mean()

# 按季度重采样
quarterly = df_ts.resample('QE').agg({
    '销售额': 'sum',
    '访问量': 'mean'
})

# 向前填充重采样
filled = df_ts.resample('D').ffill()
```

### 移动窗口计算

```python
# 滚动平均
df['7日均线'] = df['价格'].rolling(window=7).mean()

# 滚动标准差
df['30日波动率'] = df['收益率'].rolling(window=30).std()

# 指数移动平均
df['EMA'] = df['价格'].ewm(span=20).mean()

# 滚动相关性
df['相关性'] = df['X'].rolling(window=30).corr(df['Y'])
```

---

## 数据可视化

### 基础绘图

```python
import matplotlib.pyplot as plt

# 折线图
df.plot(x='日期', y='销售额', kind='line')
plt.title('销售额趋势')
plt.show()

# 柱状图
df.groupby('部门')['薪资'].mean().plot(kind='bar')
plt.title('各部门平均薪资')
plt.show()

# 散点图
df.plot(x='年龄', y='薪资', kind='scatter')
plt.show()

# 直方图
df['薪资'].plot(kind='hist', bins=20)
plt.show()
```

### 高级可视化

```python
# 子图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

df.plot(x='日期', y='销售额', ax=axes[0,0], title='销售额')
df.plot(x='日期', y='访问量', ax=axes[0,1], title='访问量')
df.groupby('部门')['薪资'].mean().plot(kind='bar', ax=axes[1,0], title='平均薪资')
df['薪资'].plot(kind='hist', ax=axes[1,1], title='薪资分布')

plt.tight_layout()
plt.show()
```

---

## 最佳实践

### 性能优化

```python
# 1. 使用适当的数据类型
df['category_col'] = df['category_col'].astype('category')
df['int_col'] = df['int_col'].astype('int32')

# 2. 避免链式索引
# ❌ 不推荐
df[df['A'] > 5]['B'] = 10

# ✅ 推荐
df.loc[df['A'] > 5, 'B'] = 10

# 3. 使用向量化操作而非 apply
# ❌ 较慢
df['new_col'] = df['col'].apply(lambda x: x * 2)

# ✅ 更快
df['new_col'] = df['col'] * 2

# 4. 合理使用 copy()
df_copy = df.copy()  # 避免视图问题
```

### 代码风格

```python
# 1. 明确的变量命名
employee_data = pd.read_csv('employees.csv')
sales_summary = employee_data.groupby('department')['salary'].mean()

# 2. 适当的注释
# 计算各部门平均薪资和员工数量
dept_stats = df.groupby('部门').agg({
    '薪资': 'mean',
    '姓名': 'count'
}).rename(columns={'姓名': '员工数'})

# 3. 错误处理
try:
    df = pd.read_csv('data.csv')
except FileNotFoundError:
    print("文件未找到")
except pd.errors.EmptyDataError:
    print("文件为空")
```

### 内存管理

```python
# 查看内存使用
print(df.info(memory_usage='deep'))

# 优化内存使用
def optimize_dtypes(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype('category')
        elif df[col].dtype == 'int64':
            df[col] = pd.to_numeric(df[col], downcast='integer')
        elif df[col].dtype == 'float64':
            df[col] = pd.to_numeric(df[col], downcast='float')
    return df

df_optimized = optimize_dtypes(df)
```

---

## 常见问题解答

### Q: 如何处理大数据集？

A:

- 使用 `chunksize` 参数分块读取
- 考虑使用 Dask 或 Vaex 库
- 优化数据类型减少内存占用

### Q: 如何提高性能？

A:

- 使用向量化操作替代循环
- 合理使用索引
- 避免不必要的数据复制

### Q: 如何处理中文编码问题？

A:

```python
# 读取时指定编码
df = pd.read_csv('chinese_data.csv', encoding='utf-8-sig')

# 保存时确保编码
df.to_csv('output.csv', encoding='utf-8-sig', index=False)
```

---

## 学习资源推荐

- [官方文档](https://pandas.pydata.org/docs/)
- [10分钟入门教程](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Cookbook](https://pandas.pydata.org/docs/user_guide/cookbook.html)

---
