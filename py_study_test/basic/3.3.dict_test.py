# encoding: utf-8

# import random

'''
序列 - 2. 元组 tuple
元组：元组属于不可变序列，不能修改元组中的元素。
'''

'''
元组的创建：
1. 基本语法{}创建   
2. dict()创建
3. zip(): zip(key, value) 创建字典对象    dict = dict(zip(key, value))
4. 通过 fromkeys 创建值为空的字典
'''
# 1.
tuple1 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
tuple2 = {}
print(tuple1)
print(tuple2)

# 2. dict()
tuple3 = dict(name='gaoqi', age=18, job='programmer')
tuple4 = dict()
print(tuple3)
print(tuple4)

# 3. zip()创建字典对象
key = ['name', 'age', 'job']
value = ['gaoqi', 18, 'techer']
tuple5 = dict(zip(key, value))
print(tuple5)

# 4. fromkeys 创建值为空的字典
tuple6 = dict.fromkeys(['name', 'age', 'job'])
print(tuple6)

'''
字典元素的访问
1. 通过 [键] 获得“值”。若键不存在，则抛出异常。
2. 通过 get()方法获得“值”。推荐使用。优点是：指定键不存在，返回 None；也可以设 定指定键不存在时默认返回的对象。推荐使用 get()获取“值对象”。
3. 列出所有的键值对
4. 列出所有的键，列出所有的值
5. len() 键值对的个数
6. 检测一个“键”是否在字典中
'''
# 1.
tuple0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
print(tuple0["name"])
# sex = tuple0["sex"]  # 不存在
# 2.
name = tuple0.get("name")
print(name)
# 3.
dict_items = tuple0.items()
print(dict_items)  # dict_items([('name', 'liuzhen'), ('age', 25), ('job', 'programmer')])
# 4.
keys = tuple0.keys()
print(keys)  # dict_keys(['name', 'age', 'job'])
# 5.
len = len(tuple0)
print(len)  # 3
# 6.
flag = "name" in tuple0
print(flag)  # True

'''
字典元素添加、修改、删除
1. 给字典新增“键值对”。如果“键”已经存在，则覆盖旧的键值对；如果“键”不存在， 则新增“键值对”。
2. 使用 update()将新字典中所有键值对全部添加到旧字典对象上。如果 key 有重复，则直 接覆盖。
3. 字典中元素的删除: 
    del(tuple["key"])  删除指定键值对，
    tuple.pop("key")  删除指定键值对，并返回对应的“值对象”
    tuple.clear() 删除所有键值对；
4. popitem() ：随机删除和返回该键值对。字典是“无序可变序列”，因此没有第一个元 素、最后一个元素的概念；popitem 弹出随机的项，因为字典并没有"最后的元素"或者其他有关顺序的概念。
若想一个接一个地移除并处理项，这个方法就非常有效（因为不用首先获取键的列表）。
'''
# 1.
tuple0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
tuple0["sex"] = "男"
tuple0["age"] = "100"
print(tuple0)  # {'name': 'liuzhen', 'age': '100', 'job': 'programmer', 'sex': '男'}
# 2. update()
b = {'name': '刘振', 'money': 100000, 'sex': '男'}
tuple0.update(b)
print(tuple0)  # {'name': '刘振', 'age': '100', 'job': 'programmer', 'sex': '男', 'money': 100000}
# 3.
del (tuple0["money"])
print(tuple0)  # {'name': '刘振', 'age': '100', 'job': 'programmer', 'sex': '男'}
sex = tuple0.pop("sex")
print(sex)  # 男
print(tuple0)  # {'name': '刘振', 'age': '100', 'job': 'programmer'}
tuple0.clear()
print(tuple0)  # {}

# 4. popitem()
tuple0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
res = tuple0.popitem()
print(res)  # ('job', 'programmer')

'''
序列解包: 序列解包可以用于元组、列表、字典。序列解包可以让我们方便的对多个变量赋值
序列解包用于字典时，默认是对“键”进行操作； 如果需要对键值对操作，则需要使用items()；如果需要对“值”进行操作，则需要使用 values()；
'''
x, y, z = (20, 30, 10)
print("x: " + str(x) + " y: " + str(y) + " z: " + str(z))
# 元组 -- 序列化包
(a, b, c) = (9, 8, 10)
print("a: " + str(a))
# 列表
[a, b, c] = [10, 20, 30]
print("a: " + str(a))
# 字典 -- 序列化包
s = {'name': '刘振', 'age': 18, 'job': 'teacher'}
name, age, job = s  # 默认对键进行操作
print(name)  # name
print(name)  # name
name, age, job = s.items()  # 对键值对进行操作
print(name)  # ('name', '刘振')
name, age, job = s.values()  # 对值进行操作
print(name)  # 刘振

'''
集合相关操作: 像数学中概念一样，Python 对集合也提供了并集、交集、差集等运算。我们给出示例
'''
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
