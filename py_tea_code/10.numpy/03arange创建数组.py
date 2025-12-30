# 导入numpy
import numpy as np

"""
arange 创建
使用 arange 函数创建数值范围并返回 ndarray 对象，函数格式如下：
numpy.arange(start, stop, step, dtype)
arange 参数说明
参数 描述
start 起始值，默认为 0
stop 终止值（不包含）
step 步长，默认为 1
dtype 返回 ndarray 的数据类型，如果没有提供，则会使用输入数据的类型。
"""

# range的使用range(start,end,step) [start,end)
a = list(range(1, 10))  # 步长是1
print(a)
b = list(range(10))  # 默认的是从0开始 ，步长是1
print(b)
c = list(range(1, 10, 3))
print(c)

# arange创建数组
# 使用arange创建1,10的数组
a = np.arange(1, 11)
print(a)

# 设置step
b = np.arange(1, 11, 2)
print(b)

# 设置dtype
c = np.arange(10, 20, 2, dtype=float)
print(c)
