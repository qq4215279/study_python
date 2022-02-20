# encoding: utf-8

import io

'''
字符串api：
ord(str) 字符串的编码 
len(str) 字符串长度
input() 从控制台读取字符串
str1 + str2 / str * n 字符串拼接
str1[n] 使用[]提取字符
replace() 实现字符串替换
str[起始偏移量 start：终止偏移量 end：步长 step] 字符串切片slice操作
    [:] 提取整个字符串                                       "abcdef"[:]     =>  "abcdef"
    [start:]从 start 索引开始到结尾                          "abcdef"[2:]    =>  "cdef"
    [:end]从头开始知道 end-1                                 "abcdef"[:2]    =>  "ab"
    [start:end:step]从 start 提取到end-1，步长是 step        "abcdef"[1:5:2] =>  "bd"
str.split() 分割
char.join(str)  合并

常用查找方法: eg: a = " 我爱编程，我喜欢写代码，学习python很快乐，高兴，666，哈哈哈！！"
len(a) 字符串长度
a.startswith("我爱") 以指定字符串开头
a.endswith('过我')  以指定字符串结尾
a.find('我')  第一次出现指定字符串的位置
a.rfind('高')  最后一次出现指定字符串的位置
a.count("编程")  指定字符串出现了几次
a.isalnum()  所有字符全是字母或数字

去除首尾信息:
a.strip(" ") 去除字符串首尾指定信息  
a.lstrip(" ")去除字符串左边指定信息
a.rstrip(" ")去除字符串右边指定信息。

大小写转换: a = "liuzhen love programming, love SXT"
a.capitalize()产生新的字符串,首字母大写
a.title()产生新的字符串,每个单词都首字母大写
a.upper()产生新的字符串,所有字符全转成大写
a.lower()产生新的字符串,所有字符全转成小写
a.swapcase()产生新的,所有字母大小写转换

格式排版：center()、ljust()、rjust()这三个函数用于对字符串实现排版

其他方法 str.api()
1. isalnum() 是否为字母或数字
2. isalpha() 检测字符串是否只由字母组成(含汉字)。
3. isdigit() 检测字符串是否只由数字组成。
4. isspace() 检测是否为空白符
5. isupper() 是否为大写字母
6. islower() 是否为小写字母


字符串的格式化 str.format() 基本语法是通过 {} 和 : 来代替以前的 % 。format 函数可以接受不限个参数，位置可以不按顺序。eg如下
填充与对齐：填充常跟对齐一起使用 
        ^、<、> 分别是居中、左对齐、右对齐，后面带宽度
        : 号后面带填充的字符，只能是一个字符，不指定的话默认是用空格填充
数字格式化：浮点数通过 f，整数通过 d 进行需要的格式化。
可变字符串：在 Python 中，字符串属于不可变对象，不支持原地修改，如果需要修改其中的值，智能创建新的字符串对象。但是，经常我们确实需要原地修改字符串，
    可以使用 io.StringIO 对象或 array 模块。
'''
binaryA = ord('A')
print(binaryA)
binaryLiu = ord("刘")
print(binaryLiu)

# myName = input("请输入你的名字：")
# print(myName)
# print(len(myName))

str1 = "a" + "b"
str2 = str1 * 3
print(str1)
print(str2)
print(str2[1])

str1 = "abadaa"
str1 = str1.replace("a", "振")
print(str1)

# 字符串切片slice操作
print("abcdefghijklmnopqrstuvwxyz"[-3:])  # 倒数三个 xyz
print("abcdefghijklmnopqrstuvwxyz"[-8:-3])  # 倒数第八个到倒数第三个(包头不包尾) stuvw
print("abcdefghijklmnopqrstuvwxyz"[::-1])  # 步长为负，从右到左反向提取 zyxwvutsrqponmlkjihgfedcba

# split()分割 和 join()合并
a = "你好 哈哈 刘振 name"
b = a.split(" ")  # ['你好', '哈哈', '刘振', 'name']
print(b)
c = "*".join(b)  # 你好*哈哈*刘振*name
print(c)

# 格式排版 center()、ljust()、rjust()
a = "LIU"
b = a.center(13, "&")
print(b)  # "&&&&&LIU&&&&&"
b = a.center(13)
print(b)  # "      LIU     "
b = a.ljust(13, "*")
print(b)  # "LIU**********"

# 字符串的格式化 str.format()
a = "我叫{0}，今年{1}岁，{0}好棒"
a = a.format("刘振", 26)
print(a)  # 我叫刘振，今年26岁，刘振好棒
b = "我的名字是{name}，年龄是{age}"
b = b.format(name="刘振", age=33)
print(b)  # 我的名字是刘振，年龄是33

# 填充与对齐
a = "{:>8}".format("256")  # "     256"
print(a)
# 数字格式化
a = "我是{0}，我的村快有{1:.2f}"
print(a.format("刘振", 10000.9999))  # 我是刘振，我的村快有10001.00
# 可变字符串: 在 Python 中，字符串属于不可变对象，不支持原地修改，如果需要修改其中的值，智能创建新的字符串对象。但是，经常我们确实需要原地修改字符串，可以使用 io.StringIO 对象或 array 模块。
s = "hello,sxt"
sio = io.StringIO(s)
value = sio.getvalue()
print("value: " + value)  # hello,sxt
seek = sio.seek(7)
print("seek: " + str(seek))  # 7  （下一步write将操作x）
sio.write('g')  # 将 x 变为 g
value = sio.getvalue()
print("value2: " + value)  # hello,sgt

'''
序列

'''
