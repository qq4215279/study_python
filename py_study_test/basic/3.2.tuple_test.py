# encoding: utf-8

"""
序列 - 2. 元组 tuple
元组：元组是一种有序、不可变的数据结构，用于存储多个元素。
使用场景： 元组适用于存储不变的数据，如坐标、日期和时间、函数返回多个值等。由于元组是不可变的，因此在某些情况下比列表更安全和更有效。

1. 元组的创建：
    1. 基本语法 () 创建   eg: my_tuple = (1, 2, 3)
    2. tuple() 创建空元组 eg: tuple()
        转换为元组：tuple(iterable)：将可迭代对象转换为元组。eg: tuple([2, 3, 4])
    3. range()创建整数列表 range([start,] end [,step])  eg: tuple(range(3));
        start 参数：可选，表示起始数字。默认是 0
        end 参数：必选，表示结尾数字。
        step 参数：可选，表示步长，默认为 1

2. 元组api
列表属于可变序列，可以任意修改列表中的元素。元组属于不可变序列，不能修改元组中的元素。因此，元组没有增加元素、修改元素、删除元素相关的方法。
因此，我们只需要学习元组的创建和删除，元组中元素的访问和计数即可。元组支持如下操作：
    tuple[index] 索引访问。元组的元素可以通过索引访问，索引从 0 开始。   eg: first_element = my_tuple[0]  # 获取第一个元素
    element in tuple：检查元素是否在元组中。
    tuple[:] 切片操作
    len(tuple) 返回元组中元素的数量。
    max() 最大值
    min() 最小值
    sum() 求和
    tuple1 + tuple2：连接操作，连接两个元组。
    tuple * n：重复元组 n 次。
    成员关系操作
    比较运算操作

3. 元组不可变性：元组的元素一旦创建就不能修改。eg: my_tuple[0] = 10  # 这会引发 TypeError，因为元组是不可变的
4. 元组拆包：可以将元组中的元素拆包赋值给多个变量。eg: my_tuple = (1, 2, 3)  x, y, z = my_tuple
5. 总结：tuple()可以接收列表、字符串、其他序列类型、迭代器等生成元组。 list()可以接收元组、字符串、其他序列类型、迭代器等生成列表
6. zip(): zip(列表 1，列表 2，...)  将多个列表对应位置的元素组合成为元组，并返回这个 zip 对象。
7. 推导式生成列表

元组遍历
    for obj in tuple:
        print(obj)
"""
# 1. 元组的创建
# 1.1  ()
tuple1 = (10, 20, 30, 50, 40)
print(tuple1)
# 1.2.1 创建一个空集合 () / tuple()
tuple2 = tuple()
print(tuple2)
# 1.2.2
tuple4 = tuple([2, 3, 4])
print(tuple4)
# 1.3. range()
tuple3 = tuple(range(3))
print(tuple3)


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

'''

for obj in tuple1:
    print(obj)

