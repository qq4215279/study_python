import pandas as pd
import numpy as np


"""
DataFrame 是 Pandas 中的另一个核心数据结构，类似于一个二维的表格或数据库中的数据表。

DataFrame 构造方法如下：

pandas.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)
参数说明：
    data：DataFrame 的数据部分，可以是字典、二维数组、Series、DataFrame 或其他可转换为 DataFrame 的对象。如果不提供此参数，则创建一个空的 DataFrame。
    index：DataFrame 的行索引，用于标识每行数据。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
    columns：DataFrame 的列索引，用于标识每列数据。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
    dtype：指定 DataFrame 的数据类型。可以是 NumPy 的数据类型，例如 np.int64、np.float64 等。如果不提供此参数，则根据数据自动推断数据类型。
    copy：是否复制数据。默认为 False，表示不复制数据。如果设置为 True，则复制输入的数据。
"""

def create_dataframe():
    # 1. 二维数组 创建DataFrame
    array = [['Google', 10], ['Runoob', 12], ['Wiki', 13]]
    df1 = pd.DataFrame(array, columns=['Site', 'Age'])
    # 使用astype方法设置每列的数据类型
    df1['Site'] = df1['Site'].astype(str)
    df1['Age'] = df1['Age'].astype(float)
    print("df1: ", df1)

    # 2.1 字典创建 DataFrame
    dict_ = {'Site': ['Google', 'Runoob', 'Wiki'], 'Age': [10, 12, 13]}
    df21 = pd.DataFrame(dict_)
    print("df21: ", df21)

    # 2.2 列表字典创建 DataFrame
    arrayDict = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}]
    df22 = pd.DataFrame(arrayDict)
    print("df22: ", df22)

    # 3. 使用 ndarrays 创建
    # 创建一个包含网站和年龄的二维ndarray
    ndarray_data = np.array([
        ['Google', 10],
        ['Runoob', 12],
        ['Wiki', 13]
    ])
    # 使用DataFrame构造函数创建数据帧
    df3 = pd.DataFrame(ndarray_data, columns=['Site', 'Age'])
    print("df3: ", df3)


"""
DataFrame 的常用操作和方法如下表所示：
    方法名称	功能描述
    head(n)	返回 DataFrame 的前 n 行数据（默认前 5 行）
    tail(n)	返回 DataFrame 的后 n 行数据（默认后 5 行）
    info()	显示 DataFrame 的简要信息，包括列名、数据类型、非空值数量等
    describe()	返回 DataFrame 数值列的统计信息，如均值、标准差、最小值等
    shape	返回 DataFrame 的行数和列数（行数, 列数）
    columns	返回 DataFrame 的所有列名
    index	返回 DataFrame 的行索引
    dtypes	返回每一列的数值数据类型
    sort_values(by)	按照指定列排序
    sort_index()	按行索引排序
    dropna()	删除含有缺失值（NaN）的行或列
    fillna(value)	用指定的值填充缺失值
    isnull()	判断缺失值，返回一个布尔值 DataFrame
    notnull()	判断非缺失值，返回一个布尔值 DataFrame
    loc[]	按标签索引选择数据
    iloc[]	按位置索引选择数据
    at[]	访问 DataFrame 中单个元素（比 loc[] 更高效）
    iat[]	访问 DataFrame 中单个元素（比 iloc[] 更高效）
    apply(func)	对 DataFrame 或 Series 应用一个函数
    applymap(func)	对 DataFrame 的每个元素应用函数（仅对 DataFrame）
    groupby(by)	分组操作，用于按某一列分组进行汇总统计
    pivot_table()	创建透视表
    merge()	合并多个 DataFrame（类似 SQL 的 JOIN 操作）
    concat()	按行或按列连接多个 DataFrame
    to_csv()	将 DataFrame 导出为 CSV 文件
    to_excel()	将 DataFrame 导出为 Excel 文件
    to_json()	将 DataFrame 导出为 JSON 格式
    to_sql()	将 DataFrame 导出为 SQL 数据库
    query()	使用 SQL 风格的语法查询 DataFrame
    duplicated()	返回布尔值 DataFrame，指示每行是否是重复的
    drop_duplicates()	删除重复的行
    set_index()	设置 DataFrame 的索引
    reset_index()	重置 DataFrame 的索引
    transpose()	转置 DataFrame（行列交换）
"""
def df_methods():
    # 创建 DataFrame
    data = {
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    }
    df = pd.DataFrame(data)

    # DataFrame 的属性和方法
    print("查看 DataFrame 的基本信息：", df.info())
    print("获取描述统计信息：", df.describe())
    print("形状：", df.shape)  # 形状
    print("列名：", df.columns)  # 列名
    print("索引：", df.index)  # 索引
    print("查看前两行数据：", df.head(2))
    print("前几行数据，默认是前 5 行：", df.head())  # 前几行数据，默认是前 5 行
    print("后几行数据，默认是后 5 行：", df.tail())  # 后几行数据，默认是后 5 行
    print("数据信息：", df.info())  # 数据信息
    print("求平均值：", df.mean())  # 求平均值
    print("求和：", df.sum())  # 求和

    # 按年龄排序
    df_sorted = df.sort_values(by='Age', ascending=False)
    print("按年龄排序：", df_sorted)

    # 选择指定列
    print("选择指定列: ", df[['Name', 'Age']])

    # 按索引选择行
    print("按索引选择行: ", df.iloc[1:3])  # 选择第二到第三行（按位置）

    # 按标签选择行
    print("按标签选择行: ", df.loc[1:2])  # 选择第二到第三行（按标签）

    # 计算分组统计（按城市分组，计算平均年龄）
    print("计算分组统计: ", df.groupby('City')['Age'].mean())

    # 处理缺失值（填充缺失值）
    df['Age'] = df['Age'].fillna(30)

    # 导出为 CSV 文件
    df.to_csv('output.csv', index=False)