# encoding: utf-8

'''
3.4 集合（Set）
集合（Set）是一种无序、可变且不重复的数据结构。
实际上，集合底层是字典实现，集合的所有元素都是字典中的“键对象”，因此是不能重复的且唯一的。集合用于存储多个不同元素的容器，它主要用于快速查找、去重和集合运算。
集合内的元素没有特定的顺序，因此不能通过索引访问。
需要注意的是，集合中的元素必须是可哈希的，这意味着集合本身不能包含可变类型的元素，如列表和其他集合。但是，集合本身是可变的，你可以向集合中添加或移除元素。

创建集合：
    1. 可以使用花括号 {}  eg: set = {3, 5, 7, 20, 100}
    2. set() 函数来创建一个集合。eg: empty_set = set()

添加和移除元素：
    set.add(element)：向集合中添加元素。
    set.remove(element)：从集合中移除指定元素，如果元素不存在会引发 KeyError。
    set.discard(element)：从集合中移除指定元素，如果元素不存在不会引发异常。
    set.pop()：移除并返回任意一个元素，集合为空时引发 KeyError。
    set.clear()：移除集合中的所有元素。

集合操作：
    交集：set1 & set2 或 set1.intersection(set2)
    并集：set1 | set2 或 set1.union(set2)
    差集：set1 - set2 或 set1.difference(set2)
    对称差集（只存在于一个集合中的元素）：set1 ^ set2 或 set1.symmetric_difference(set2)
    子集检查：set1.issubset(set2)
    超集检查：set1.issuperset(set2)

其他方法：
    len(set)：返回集合中元素的数量。
    element in set：检查元素是否在集合中。


'''
# 集合的创建
# 1.1 使用 {} 创建集合对象，并使用 add()方法添加元素
a = {3, 5, 7, 20, 100}


# 1.2. 使用 set()，将列表、元组等可迭代对象转成集合。如果原来数据存在重复数据，则只保 留一个。
list = ['a', 'b', 'c', 'b']
b = set(list)

# 2. add() 添加
a.add(100)
print("aa: ", a)  # aa:  {3, 100, 5, 7, 20}

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
