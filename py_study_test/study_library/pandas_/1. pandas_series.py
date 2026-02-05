import pandas as pd
import numpy as np

"""
Series 是 Pandas 中的一个核心数据结构，类似于一个一维的数组，具有数据和索引。
创建 Series
    可以使用 pd.Series() 构造函数创建一个 Series 对象，传递一个数据数组（可以是列表、NumPy 数组等）和一个可选的索引数组。
    pandas.Series(data=None, index=None, dtype=None, name=None, copy=False, fastpath=False)
    参数说明：
        data：Series 的数据部分，可以是列表、数组、字典、标量值等。如果不提供此参数，则创建一个空的 Series。
        index：Series 的索引部分，用于对数据进行标记。可以是列表、数组、索引对象等。如果不提供此参数，则创建一个默认的整数索引。
        dtype：指定 Series 的数据类型。可以是 NumPy 的数据类型，例如 np.int64、np.float64 等。如果不提供此参数，则根据数据自动推断数据类型。
        name：Series 的名称，用于标识 Series 对象。如果提供了此参数，则创建的 Series 对象将具有指定的名称。
        copy：是否复制数据。默认为 False，表示不复制数据。如果设置为 True，则复制输入的数据。
        fastpath：是否启用快速路径。默认为 False。启用快速路径可能会在某些情况下提高性能。


"""


def create_series():
    # 1. 使用列表创建 Series
    s1 = pd.Series([1, 2, 3, 4])
    # 读取列数据
    print(s1[1])
    print("s1[1]: ", s1[1])

    # 指定索引值，如下实例：
    a = ["Google", "Runoob", "Wiki"]
    s11 = pd.Series(a, index=["x", "y", "z"])
    print("s2: ", s11)

    # 2. 字典创建 Series
    sites = {1: "Google", 2: "Runoob", 3: "Wiki"}
    s2 = pd.Series(sites, index=[1, 2])
    print("s2: ", s2)

    # 3. 使用 NumPy 数组创建 Series
    s3 = pd.Series(np.array([1, 2, 3, 4]))
    print("s3 ", s3)



"""
方法名称	功能描述
index	获取 Series 的索引
values	获取 Series 的数据部分（返回 NumPy 数组）
head(n)	返回 Series 的前 n 行（默认为 5）
tail(n)	返回 Series 的后 n 行（默认为 5）
dtype	返回 Series 中数据的类型
shape	返回 Series 的形状（行数）
describe()	返回 Series 的统计描述（如均值、标准差、最小值等）
isnull()	返回一个布尔 Series，表示每个元素是否为 NaN
notnull()	返回一个布尔 Series，表示每个元素是否不是 NaN
unique()	返回 Series 中的唯一值（去重）
value_counts()	返回 Series 中每个唯一值的出现次数
map(func)	将指定函数应用于 Series 中的每个元素
apply(func)	将指定函数应用于 Series 中的每个元素，常用于自定义操作
astype(dtype)	将 Series 转换为指定的类型
sort_values()	对 Series 中的元素进行排序（按值排序）
sort_index()	对 Series 的索引进行排序
dropna()	删除 Series 中的缺失值（NaN）
fillna(value)	填充 Series 中的缺失值（NaN）
replace(to_replace, value)	替换 Series 中指定的值
cumsum()	返回 Series 的累计求和
cumprod()	返回 Series 的累计乘积
shift(periods)	将 Series 中的元素按指定的步数进行位移
rank()	返回 Series 中元素的排名
corr(other)	计算 Series 与另一个 Series 的相关性（皮尔逊相关系数）
cov(other)	计算 Series 与另一个 Series 的协方差
to_list()	将 Series 转换为 Python 列表
to_frame()	将 Series 转换为 DataFrame
iloc[]	通过位置索引来选择数据
loc[]	通过标签索引来选择数据
"""
def series_api():
    # 创建 Series
    data = [1, 2, 3, 4, 5, 6]
    index = ['a', 'b', 'c', 'd', 'e', 'f']
    s = pd.Series(data, index=index)

    # 查看基本信息
    print("获取索引：", s.index)
    print("获取值数组：", s.values)
    print("数据类型：", s.dtype)
    # 其他属性和方法
    print("形状：", s.shape)  # 形状
    print("元素个数：", s.size)  # 元素个数
    print("前几个元素，默认是前 5 个：", s.head())  # 前几个元素，默认是前 5 个
    print("前两行数据：", s.head(2))
    print("后几个元素，默认是后 5 个：", s.tail())  # 后几个元素，默认是后 5 个

    print("求和：", s.sum())  # 求和
    print("平均值：", s.mean())  # 平均值
    print("标准差：", s.std())  # 标准差
    print("最小值：", s.min())  # 最小值
    print("最大值：", s.max())  # 最大值
    print("获取描述统计信息：", s.describe())  # 最大值
    print("获取最大值的索引：", s.idxmax())  # 最大值
    print("获取最小值的索引：", s.idxmin())  # 最大值

    # 使用 map 函数将每个元素加倍
    s_doubled = s.map(lambda x: x * 2)
    print("元素加倍后：", s_doubled)
    # 计算累计和
    cumsum_s = s.cumsum()
    print("累计求和：", cumsum_s)
    # 查找缺失值（这里没有缺失值，所以返回的全是 False）
    print("缺失值判断：", s.isnull())
    # 排序
    sorted_s = s.sort_values()
    print("排序后的 Series：", sorted_s)


"""
基本操作：
"""
def base_op():
    # 指定索引创建 Series
    s = pd.Series([1, 2, 3, 4], index=['a', 'b', 'c', 'd'])

    # 获取值
    value = s[2]  # 获取索引为2的值
    print(s['a'])  # 返回索引标签 'a' 对应的元素

    # 获取多个值
    subset = s[1:4]  # 获取索引为1到3的值

    # 使用自定义索引
    value = s['b']  # 获取索引为'b'的值

    # 索引和值的对应关系
    for index, value in s.items():
        print(f"Index: {index}, Value: {value}")

    # 使用切片语法来访问 Series 的一部分
    print(s['a':'c'])  # 返回索引标签 'a' 到 'c' 之间的元素
    print(s[:3])  # 返回前三个元素

    # 为特定的索引标签赋值
    s['a'] = 10  # 将索引标签 'a' 对应的元素修改为 10

    # 通过赋值给新的索引标签来添加元素
    s['e'] = 5  # 在 Series 中添加一个新的元素，索引标签为 'e'

    # 使用 del 删除指定索引标签的元素。
    del s['a']  # 删除索引标签 'a' 对应的元素

    # 使用 drop 方法删除一个或多个索引标签，并返回一个新的 Series。
    s_dropped = s.drop(['b'])  # 返回一个删除了索引标签 'b' 的新 Series

    # 计算统计数据：使用 Series 的方法来计算描述性统计。
    print("s.sum: ", s.sum())  # 输出 Series 的总和
    print("s.mean: ", s.mean())  # 输出 Series 的平均值
    print("s.max: ", s.max())  # 输出 Series 的最大值
    print("s.min: ", s.min())  # 输出 Series 的最小值
    print("s.std: ", s.std())  # 输出 Series 的标准差

