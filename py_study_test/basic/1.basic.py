# encoding: utf-8

import time
import io
import platform
import yaml
import copy


"""
命名规则
1. 模块名和包名：全小写字母，尽量简单。若多个单词之间用下划线。eg：math, os, sys
2. 类名：首字母大写，多个单词之间采用驼峰原则（多个单词时，每个单词第一个字母大写，其余部分小写）。eg：MyPhone, User
   - 实例名，全小写字母，尽量简单。
   - 每个类，应紧跟“文档字符串”，说明这个类的作用。
   - 可以用空行组织代码，但不能滥用。在类中，使用一个空行隔开方法；模块中，使用两个空行隔开多个类。
3. 函数名：全小写字母，多个单词之间用下划线隔开。eg：play_phone(), do_work(),
4. 常量名：全大写字母，多个单词使用下划线隔开。eg：SPEED、MAX_SPEED
"""



'''
Python中，一切皆对象。每个对象由：标识（identity）、类型（type）、value（值） 组成。
id(obj): 返回对象 obj 的标识。
type(obj): 获得对象的所属类型。
print(obj): 直接打印出值。

常见的内置数据类型：
    整数类型 (int): 表示整数，例如：42, -10, 0.
    浮点数类型 (float): 表示浮点数，例如：3.14, -0.5, 2.0.
    复数类型 (complex): 表示复数，例如：3 + 4j, -2 - 7j.
    字符串类型 (str): 表示文本，例如："hello", 'Python'.
    布尔类型 (bool): 表示布尔值，即 True 或 False.
    列表类型 (list): 表示有序可变序列，例如：[1, 2, 3], ["a", "b", "c"].
    元组类型 (tuple): 表示有序不可变序列，例如：(1, 2, 3), ("apple", "banana").
    字典类型 (dict): 表示键-值对的映射，例如：{"name": "Alice", "age": 30}, {1: "one", 2: "two"}.
    集合类型 (set): 表示无序的、不重复的元素集合，例如：{1, 2, 3}, {"apple", "banana"}.
    字节类型 (bytes): 表示字节序列，例如：b'hello', b'\x01\x02\x03'.
    字节数组类型 (bytearray): 表示可变的字节序列，类似于 bytes 类型。
    None 类型 (NoneType): 表示空值或缺失值，仅有一个值 None.
    函数类型 (function): 表示函数对象。
    模块类型 (module): 表示模块对象，例如：math, os.
    类类型 (class): 表示类对象，例如：str, int.
    实例类型 (instance): 表示类的实例对象，例如："hello" 是 str 类的实例。
    生成器类型 (generator): 表示生成器对象，用于生成迭代序列的值。

type() 查看任意对象的类型，例如：type(42) 返回 <class 'int'>。
isinstance(obj, type) 判断一个对象是否属于指定的类型。接受两个参数：要检查的对象和要检查的类型，如果对象是指定类型的实例，则返回 True，否则返回 False。
'''
print(id(2))  # 1440458688
print(type(2))  # <class 'int'>

# 检查整数类型
print("是否是整数类型：", isinstance(42, int))  # 输出: True
print("是否是字符串类型：", isinstance("字符串", str))  # 输出: True

true = True
# 取反操作 not 关键字
false = not true
print("取反操作：", false)

# 换行符：\
s = '我是一个字符串，' \
    '可以换行的字符串'
print(s)

# 可换行的字符串：""" 或 '''
sql = """create table t_person(
          pno INTEGER primary key autoincrement,
          pname VARCHAR not null,
          age INTEGER 
      )"""
print("sql: ", sql)

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
# x = int(input("请输入一个数字\n"))
# print("输入的数字：", x)


"""
pass 是 Python 中的一个关键字，它是一个空语句，用于在代码块中占位或表示空操作。在某些情况下，语法要求有语句存在，但你又不想执行任何实际的操作时，可以使用 pass 关键字。
    eg: class MyClass:
            pass
"""

"""
转义字符 我们可以使用“ \\ + 特殊字符 ”，实现某些难以用字符表示的效果。比如：换行等。常见的转义字符有这些：
\(在行尾时)  | 续行符
\\: 表示一个普通的反斜杠。
\': 表示单引号。
\": 表示双引号。
\b: 表示退格符，用于在字符串中创建退格。
\n: 表示换行符，用于在字符串中创建一个新行。
\t: 表示制表符，用于在字符串中创建水平制表。
\r: 表示回车符，将光标移到当前行的开头。
\f: 表示换页符，用于在字符串中创建分页。
\v: 表示垂直制表符。
"""
print("Hello\nWorld")  # 换行
print("This is a\ttab.")  # 制表
print("She said, \"Hello!\"")  # 引号

"""
拷贝
浅拷贝：不拷贝子对象的内容，只是拷贝子对象的引用。
深拷贝：会连子对象的内存也全部拷贝一份，对子对象的修改不会影响源对象
"""
a = [10, 20, [1, 2]]
b = copy.copy(a)
print("a == b:", a == b)
print("a is b:", a is b)

c = copy.deepcopy(a)
print("a == c:", a == c)
print("a is c:", a is c)
