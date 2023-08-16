# encoding: utf-8

"""
3.3 字典 dict

1. 元组的创建：
    1. 基本语法{}创建 eg: dict = {"name": "Alice", "age": 30, "city": "New York"}
    2. dict()创建。eg: tuple = [("a", 1), ("b", 2), ("c", 3)] converted_dict = dict(tuple)
    3. zip(): zip(key, value) 创建字典对象    dict = dict(zip(key, value))
    4. 通过 fromkeys 创建值为空的字典

2. 字典元素的访问
    key in dict 检测一个“键”是否在字典中
    dict.get(key) 通过 get()方法获得“值”。推荐使用。优点是：指定键不存在，返回 None；也可以设定指定键不存在时默认返回的对象。推荐使用 get()获取“值对象”。eg: name = dict.get("name")
    dict[key] 若键不存在，则抛出异常。eg: name = my_dict["name"]
    dict.keys() 列出所有的键值对
    dict.values() 返回字典中所有值的列表。
    dict.items() 列出所有的键，列出所有的值
    len() 键值对的个数
    遍历字典：使用循环遍历字典的键或键-值对。
        for key in dict:
            value = dict[key]

3. 字典元素添加、修改
    dict[key] = value  添加或修改。给字典新增“键值对”。如果“键”已经存在，则覆盖旧的键值对；如果“键”不存在， 则新增“键值对”。
    dict.update(dict0)  使用 update()将新字典中所有键值对全部添加到旧字典对象上。如果 key 有重复，则直接覆盖。

4. 字典中元素的删除:
    del(dict["key"])  删除指定键值对，
    dict.pop("key")  删除指定键值对，并返回对应的“值对象”
    dict.clear() 删除所有键值对；
    dict.popitem() ：随机删除和返回该键值对。字典是“无序可变序列”，因此没有第一个元素、最后一个元素的概念；popitem 弹出随机的项，因为字典并没有"最后的元素"或者其他有关顺序的概念。
        若想一个接一个地移除并处理项，这个方法就非常有效（因为不用首先获取键的列表）。

5. 序列解包: 序列解包可以用于元组、列表、字典。序列解包可以让我们方便的对多个变量赋值
    序列解包用于字典时，默认是对“键”进行操作； 如果需要对键值对操作，则需要使用items()；如果需要对“值”进行操作，则需要使用 values()；
"""

"""
1. 字典的创建
"""
# 1.1.
dict1 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
dict2 = {}
print(dict1)
print(dict2)

# 1.2. dict()
dict3 = dict(name='gaoqi', age=18, job='programmer')
dict4 = dict()
print(dict3)
print(dict4)

# 1.3. zip()创建字典对象
key = ['name', 'age', 'job']
value = ['gaoqi', 18, 'techer']
dict5 = dict(zip(key, value))
print(dict5)

# 1.4. fromkeys 创建值为空的字典
dict6 = dict.fromkeys(['name', 'age', 'job'])
print(dict6)


"""
2. 字典元素的访问
"""
dict0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
# 2.1.
flag = "name" in dict0
print(flag)  # True
# 2.2.
name = dict0.get("name")
print(name)
# 2.3
print(dict0["name"])
# sex = tuple0["sex"]  # 不存在
# 2.4.
keys = dict0.keys()
print("keys: ", keys)  # dict_keys(['name', 'age', 'job'])
# 2.5.
values = dict0.values()
print("values: ", values)
# 2.6.
dict_items = dict0.items()
print("dict_items: ", dict_items)  # dict_items([('name', 'liuzhen'), ('age', 25), ('job', 'programmer')])
# 2.7.
len = len(dict0)
print(len)  # 3


'''
3. 字典元素添加、修改
'''
# 3.1.
dict0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
dict0["sex"] = "男"
dict0["age"] = "100"
print(dict0)  # {'name': 'liuzhen', 'age': '100', 'job': 'programmer', 'sex': '男'}
# 3.2. update()
b = {'name': '刘振', 'money': 100000, 'sex': '男'}
dict0.update(b)
print(dict0)  # {'name': '刘振', 'age': '100', 'job': 'programmer', 'sex': '男', 'money': 100000}

"""
4. 字典的删除
"""
# 4.1. del(dict(key))
del(dict0["money"])
print(dict0)  # {'name': '刘振', 'age': '100', 'job': 'programmer', 'sex': '男'}
# 4.2. pop(key)
sex = dict0.pop("sex")
print(sex)  # 男
print(dict0)  # {'name': '刘振', 'age': '100', 'job': 'programmer'}
# 4.3. clear()
dict0.clear()
print(dict0)  # {}
# 4.4. popitem()
dict0 = {'name': 'liuzhen', 'age': 25, 'job': 'programmer'}
res = dict0.popitem()
print(res)  # ('job', 'programmer')

'''
5. 序列解包
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
