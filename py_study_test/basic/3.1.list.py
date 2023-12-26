# encoding: utf-8

import random

'''
序列 - 1. 列表 list
列表：用于存储任意数目、任意类型的数据集合。
'''

'''
列表的创建：
1. 基本语法[]创建
2. list()创建
3. range()创建整数列表 range([start,] end [,step])
    start 参数：可选，表示起始数字。默认是 0
    end 参数：必选，表示结尾数字。
    step 参数：可选，表示步长，默认为 1
4. 推导式生成列表(简介一下，重点在for循环后讲)    
'''
# 1.
list1 = [10, 30, 20, 50]
print(list1)
# 2. 创建一个空集合 [] / list()
list2 = []
print(list2)
list3 = list()
print(list3)
# 3. range()
list4 = list(range(3, 15, 2))
print(list4)  # [3, 5, 7, 9, 11, 13]
list5 = list(range(15, 3, -1))
print(list5)  # [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4]
list6 = list(range(3, -10, -1))
print(list6)  # [3, 2, 1, 0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
# 4. 推导
list7 = [x * 2 for x in range(5)]  # 循环创建多个元素
print(list7)  # [0, 2, 4, 6, 8]
list8 = [x * 2 for x in range(100) if x % 9 == 0]  # 通过 if 过滤元素
print(list8)  # [0, 18, 36, 54, 72, 90, 108, 126, 144, 162, 180, 198]
print("------------------------------------>")

'''
列表api：
    list.append(x)          增加元素            将元素 x 增加到列表 list 尾部
    list.extend(aList)      增加元素            将列表 alist 所有元素加到列表 list 尾部
    list.insert(index, x)   增加元素            在列表 list 指定位置 index 处插入元素 x
    list2 = list * n        增加元素            乘法扩展，使用乘法扩展列表，生成一个新列表，新列表元素时原列表元素的多次重复。
    
    list.remove(x)          删除元素            在列表 list 中删除首次出现的指定元素 x
    list.pop(index)       删除元素            删除并返回列表 list 指定为止 index 处的元素，默认是最后一个元素
    del list[index]         删除元素            del list[1]
    list.clear()            删除所有元素        删除列表所有元素，并不是删除列表对象
   
    list[index]             访问元素            list[1]
    list.index(value, [start,[end]])           获取指定元素首次出现的索引位置。其中， start 和 end 指定了搜索的范围。若不存在 value 元素抛出异常
    
    len(list)               列表长度            返回列表中包含元素的个数
    list.count(x)           计数                返回指定元素 x 在列表 list 中出现的次数
    list.sort()             排序                所有元素原地排序
    list.reverse()          翻转列表            所有元素原地翻转
    list.copy()             浅拷贝              返回列表对象的浅拷贝

切片操作: 切片 slice 操作可以让我们快速提取子列表或修改。标准格式为：[起始偏移量 start:终止偏移量 end[:步长 step]]
    [:] 提取整个列表                                                 [10,20,30][:]                        [10,20,30]
    [start:]从 start 索引开始到结尾                                  [10,20,30][1:]                       [20,30]
    [:end]从头开始知道 end-1                                         [10,20,30][:2]                       [10,20]
    [start:end]从 start 到 end-1                                     [10,20,30,40][1:3]                   [20,30]
    [start:end:step] 从 start 提取到 end-1，步长是 step              [10,20,30,40,50,60,70][1:6:2]         [20, 40, 60]

+ 运算符操作: 并不是真正的尾部添加元素，而是创建新的列表对象；将原列表的元素和新列表的元素依次 复制到新的列表对象中。这样，会涉及大量的复制操作，对于操作大量元素不建议使用。
    list = list + [200]

列表的遍历 
    for obj in listObj:
	    print(obj)
    
    for i in range(len(listObj)):
        print(listObj[i])
	    
列表排序 
升序：
    1. list.sort()  # 默认是升序排列
    2. list = sorted(list) # 默认升序
降序：
    1. list.sort(reverse=True) # 降序排列
    2. list = reversed(list) # 内置函数 reversed()也支持进行逆序排列，与列表对象 reverse()方法不同的是，内置函数reversed()不对原列表做任何修改，只是返回一个逆序排列的迭代器对象。

打乱顺序
    import random    
    random.shuffle(list)

列表相关的其他内置函数汇总
    max(list) 返回列表中最大值。
    min(list) 返回列表中最小值。
    sum(list) 对数值型列表的所有元素进行求和操作，对非数值型列表运算则会报错。
'''
list = [10, 20, 50, 20, 20]
# append()
list.append(100)
print(list)  # [10, 20, 50, 100]

# extend() 将目标列表的所有元素添加到本列表的尾部，属于原地操作，不创建新的列表对象。
print("id(list)前: " + str(id(list)))  # id(list)前: 26557960
list.extend([120, 150])
print("id(list)后: " + str(id(list)))  # id(list)后: 26557960

# +运算符操作  结论：a 的地址发生了变化。也就是创建了新的列表对象。
a = [20, 50]
print("id(a): " + str(id(a)))  # id(a): 22821992
b = a + [100]
print("id(b): " + str(id(b)))  # id(b): 22831720

# insert() 插入元素
# 使用 insert()方法可以将指定的元素插入到列表对象的任意制定位置。这样会让插入位置后面所有的元素进行移动，会影响处理速度。涉及大量元素时，尽量避免使用。
# 类似发生这种移动的函数还有：remove()、pop()、del()，它们在删除非尾部元素时也会发生操作位置后面元素的移动。
list.insert(2, 100)

# 乘法扩展 使用乘法扩展列表，生成一个新列表，新列表元素时原列表元素的多次重复。
a = ['sxt', 100]
b = a * 3
print(a)  # ['sxt', 100]
print(b)  # ['sxt', 100, 'sxt', 100, 'sxt', 100]

# 列表元素的删除
del list[1]  # 删除列表指定位置的元素。
# pop() 删除并返回指定位置元素，如果未指定位置则默认操作列表最后一个元素。
num = list.pop()
print(num)
# remove() 删除首次出现的指定元素，若不存在该元素抛出异常。
list.remove(100)

# 访问元素
num = list[1]
print(num)

# index()获得指定元素在列表中首次出现的索引 语法是：index(value,[start,[end]])。其中， start 和 end 指定了搜索的范围。
print(list.index(20))
print(list.index(20, 2))
print(list.index(20, 2, 5))

# count()获得指定元素在列表中出现的次数 count()可以返回指定元素在列表中出现的次数。
count = list.count(20)
print(count)
# 成员资格判断 判断列表中是否存在指定的元素，我们可以使用 count()方法，返回 0 则表示不存在，返回大于 0 则表示存在。但是，一般我们会使用更加简洁的 in 关键字来判断，直接返回 True或 False。
flag = 20 in list
print(flag)

print("开始遍历列表：")
for num in list:
    print(num)
print("结束遍历列表===========>")

print("开始遍历列表2：")
for i in range(len(list)):
    print("i: " + str(i) + " value: ", list[i])
print("结束遍历列表===========>")

'''
切片操作
'''
print("切片操作：======>")
# 其他操作（三个量为负数）的情况：
# 倒数三个
print([10, 20, 30, 40, 50, 60, 70][-3:])  # [50, 60, 70]
# 倒数第五个到倒数第三个(包头不包尾)
print([10, 20, 30, 40, 50, 60, 70][-5: -3])  # [30, 40]
# 步长为负，从右到左反向提取
print([10, 20, 30, 40, 50, 60, 70][::-1])  # [70, 60, 50, 40, 30, 20, 10]

'''
列表排序 
升序：
1. list.sort()  默认是升序排列
2. list = sorted(list) # 默认升序
降序：
1. list.sort(reverse=True) # 降序排列
2. list = reversed(list) # 内置函数 reversed()也支持进行逆序排列，与列表对象 reverse()方法不同的是，内置函数reversed()不对原列表做任何修改，只是返回一个逆序排列的迭代器对象。

打乱顺序
import random    random.shuffle(list)
'''
print("排序：")
list.sort()  # [10, 20, 20, 50, 100, 120]
print(list)
list.sort(reverse=True)
print(list)  # [120, 100, 50, 20, 20, 10]
list = sorted(list)
print(list)  # [10, 20, 20, 50, 100, 120]
list_reversed = reversed(list)
print(list_reversed)  # <list_reverseiterator object at 0x0150C0A0>

# random.shuffle(list)  打乱顺序
random.shuffle(list)
print(list)  # [20, 120, 100, 50, 10, 20]

print("列表相关的其他内置函数===>")
print(max(list))  # 120
print(min(list))  # 10
print(sum(list))  # 320

