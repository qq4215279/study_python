# 导入numpy模块
import numpy as np


"""
数组的创建
array 创建
numpy 模块的 array 函数可以生成多维数组。例如，如果要生成一个二维数组，需要向
array 函数传递一个列表类型的参数。每一个列表元素是一维的 ndarray 类型数组，作为二维
数组的行。另外，通过 ndarray 类的 shape 属性可以获得数组每一维的元素个数（元组形式），
也可以通过 shape[n]形式获得每一维的元素个数，其中 n 是维度，从 0 开始。
语法格式如下：
numpy.array(object, dtype = None, copy = True, order = None, subok = False, ndmin = 0)
array 参数说明
名称 描述
object 数组或嵌套的数列
dtype 数组元素的数据类型，可选
copy 对象是否需要复制，可选
order 创建数组的样式，C 为行方向，F 为列方向，A 为任意方向（默认）
subok 默认返回一个与基类类型一致的数组
ndmin 指定生成数组的最小维度
"""

# 使用array函数创建一维数组
a = np.array([1, 2, 3, 4])
print(a)
print(type(a))

# 使用array函数创建二维数组
b = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(b)
print(type(b))

# 使用array函数创建三维数组
c = np.array([[[1, 2, 3], [4, 5, 6], [7, 8, 9]]])
print(c)
print(type(c))

# array函数中dtype的使用
d = np.array([3, 4, 5], dtype=float)
print(d)
print(type(d))

# array函数中ndim的使用
e = np.array([5, 6, 7], dtype=float, ndmin=3)
print(e)
