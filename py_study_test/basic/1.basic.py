# encoding: utf-8

import time
import io
import platform
import yaml

# 换行符：\
s = '我是一个字符串，' \
    '可以换行的字符串'
print(s)

# 打印python版本号
print(platform.python_version())

# 可换行的字符串：""" 或 '''
sql = """create table t_person(
          pno INTEGER primary key autoincrement,
          pname VARCHAR not null,
          age INTEGER 
      )"""
print("sql: ", sql)

'''
Python中，一切皆对象。**每个对象由：标识（identity）、类型（type）、value（值） 组成。
id(obj): 返回对象 obj 的标识。
type(obj): 获得对象的所属类型。
print(obj): 直接打印出值。
'''
print(id(2))
print(type(2))

'''
定义变量
'''
a = 123
b = 124
# 链式赋值
x = y = 120

'''
int类型转换：int(str)
'''
a1 = 0b11111
a2 = "999"
print(int(a1))
print(int(a2))
# 在python3以上，浮点数也可以自动转换
print(int(345.999))
# 四舍五入
print(round(345.999))

'''
时间的表示: time.time()
'''
print(time.time())

'''
运算符：is 于 is not
is 是判断两个标识符是不是引用同一个对象
is not 是判断两个标识符是不是引用不同对象

is 与 == 区别：
- is 用于判断两个变量引用对象是否为同一个，既比较对象的地址。
- == 用于判断引用变量引用对象的值是否相等，默认调用对象的 __eq__()方法。
'''
str1 = "字符串1"
str11 = "字符串1"
str2 = "字符串2"
print(str1 is str11)  # True
print(str1 == str11)  # True

# input()
x = int(input("请输入一个数字"))
print("输入的数字：", x)