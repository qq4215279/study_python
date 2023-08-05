# encoding: utf-8

# import random

'''
序列 - 2. 元组 tuple
元组：元组属于不可变序列，不能修改元组中的元素。
'''

'''
元组的创建：
1. 基本语法()创建
2. tuple()创建
3. range()创建整数列表 range([start,] end [,step])
    start 参数：可选，表示起始数字。默认是 0
    end 参数：必选，表示结尾数字。
    step 参数：可选，表示步长，默认为 1
4. 总结：tuple()可以接收列表、字符串、其他序列类型、迭代器等生成元组。 list()可以接收元组、字符串、其他序列类型、迭代器等生成列表  
5. zip(): zip(列表 1，列表 2，...)  将多个列表对应位置的元素组合成为元组，并返回这个 zip 对象。
5. 推导式生成列表
'''
# 1.
tuple1 = (10, 20, 30, 50, 40)
print(tuple1)
# 2. 创建一个空集合 () / tuple()
tuple2 = tuple()
print(tuple2)
# 3. range()
tuple3 = tuple(range(3))
print(tuple3)
tuple4 = tuple([2, 3, 4])
print(tuple4)
# 4.

# 5. zip()
a = [40, 50]
b = [10, 400]
c = [111, 999]
zipObj = zip(a, b, c)
tuple5 = list(zipObj)
print(zipObj)  # <zip object at 0x018C3968>
print(tuple5)  # [(40, 10, 111), (50, 400, 999)]

'''
元组api
列表属于可变序列，可以任意修改列表中的元素。元组属于不可变序列，不能修改元组中的元素。因此，元组没有增加元素、修改元素、删除元素相关的方法。
因此，我们只需要学习元组的创建和删除，元组中元素的访问和计数即可。元组支持如下操作：
1. 索引访问         tuple[index]
2. 切片操作         tuple[:]
3. 连接操作         
4. 成员关系操作
5. 比较运算操作
6. 计数：元组长度 len()、最大值 max()、最小值 min()、求和 sum()等。
'''


'''
3.4 集合
集合是无序可变，元素不能重复。实际上，集合底层是字典实现，集合的所有元素都是字典中的“键对象”，因此是不能重复的且唯一的。
'''
# 1. 使用{}创建集合对象，并使用 add()方法添加元素
a = {3, 5, 7, 20, 100}
a.add(9)

# 2. 使用 set()，将列表、元组等可迭代对象转成集合。如果原来数据存在重复数据，则只保 留一个。
list = ['a','b','c','b']
b = set(list)

# 3. remove()删除指定元素；clear()清空整个集合
a.remove(20)
print("a: ", a)
a.clear()
print("a: ", a)

# 集合相关操作: 像数学中概念一样，Python 对集合也提供了并集、交集、差集等运算。我们给出示例
a = {1, 3, 'sxt'}
b = {'he', 'it', 'sxt'}
# 并集
c = a | b
print(c)  # {1, 3, 'sxt', 'he', 'it'}
# 交集
c = a & b
print(c)  # {'sxt'}
# 差集
c = a - b
print(c)  # {1, 3}
# 并集
c = a.union(b)
print(c)  # {1, 3, 'sxt', 'he', 'it'}
# 交集
c = a.intersection(b)
print(c)  # {'sxt'}
# 差集
c = a.difference(b)
print(c)  # {1, 3}