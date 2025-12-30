#!/usr/bin/env python
# encoding: utf-8

'''
函数用法
'''

'''
函数定义：
def 函数名([参数列表]) :
	文档字符串
	函数体/若干语句
'''


def findMax(a, b):
    max = 0
    if a > b:
        print(a)
        max = a
    else:
        print(b)
        max = b
    return max, "多个返回值！！"


max = findMax(10, 77)
print("many return test: ")
print(max)
print(max[1])

# 定义逻辑常量
CONSTANT_A = 100

'''
函数内，修改常量需要用 global 关键字修饰
文档字符串(函数的注释): 程序的可读性最重要，一般建议在函数体开始的部分附上函数定义说明，这就是“文档字符串”，也有人成为“函数的注释”。我们通过三个单引号或者三个双引号来实现，
    中间可以加入多行文字进行说明。 
    调用 help(函数名.__doc__) 可以打印输出函数的文档字符串。
'''


def f1():
    global CONSTANT_A
    print(CONSTANT_A)
    ''' 修改常量的值 -- help(f1.__doc__) '''
    CONSTANT_A = 300
    print(CONSTANT_A)


f1()
# help(f1.__doc__)

'''
参数的几种类型:
1. 位置参数 函数调用时，实参默认按位置顺序传递，需要个数和形参匹配。按位置传递的参数，称为： “位置参数”。
2. 默认值参数  这些参数在传递时就是可选的。称为“默认值参数”。 默认值参数放到位置参数后面
3. 命名参数 按照形参的名称传递参数，称为“命名参数”，也称“关键字参数”。
4. 可变参数
    可变参数指的是“可变数量的参数”。分两种情况：
        1. *param（一个星号），将多个参数收集到一个“元组”对象中。
        2. **param（两个星号），将多个参数收集到一个“字典”对象中。
5. 强制命名参数 在带星号的“可变参数”后面增加新的参数，必须在调用的时候“强制命名参数”。
'''


# 1. 位置参数
def f1(a, b, c):
    print("位置参数: ")
    print(a, b, c)


f1(2, 3, 4)


# f2(2, 3)  # 报错， 位置参数不正确

# 2. 默认值参数
def f2(a, b, c=10, d=20):
    print("默认值参数: ")
    print(a, b, c, d)


f2(8, 9)
f2(8, 9, 20)
f2(8, 9, 20, 40)


# 3. 命名参数
def f3(a, b, c):
    print("命名参数: ")
    print(a, b, c)


f3(1, 8, 9)  # 位置参数
f3(c=100, a=200, b=300)  # 命名参数


# 4. 可变参数
def f4_1(a, b, *c):
    print("f4_1: ")
    print(a, b, c)


def f4_2(a, b, **c):
    print("f4_2: ")
    print(a, b, c)


def f4_3(a, b, *c, **d):
    print("f4_3: ")
    print(a, b, c, d)


f4_1(1, 2, 5, 60)
f4_2(8, 9, name="liuzhen", age=20)
f4_3(8, 9, 20, 30, name="liuzhen", age=20)


# 5. 强制命名参数
def f5(*a, b, c):
    print("强制命名参数: ")
    print(a, b, c)


# f5(2,4,5)  # 会报错，因为a是可变参数，将4,5 全部收集，造成b,c没有赋值
f5(2, b=10, c=20)  # (2,) 10 20

'''
lambda 表达式和匿名函数
lambda 表达式可以用来声明匿名函数。lambda 函数是一种简单的、在同一行中定义函数 的方法。lambda 函数实际生成了一个函数对象。lambda 表达式只允许包含一个表达式，不能包含复杂语句，
该表达式的计算结果就是函数的返回值。
lambda 表达式的基本语法如下：lambda arg1,arg2,arg3... : <表达式>
arg1/arg2/arg3 为函数的参数。<表达式>相当于函数体。运算结果是：表达式的运算结果。
'''
print("lambda 表达式 test")
f6 = lambda a, b, c: a + b + c
print(f6)  # <function <lambda> at 0x016DF268>
print(f6(2, 5, 6))  # 13

f7 = [lambda a: a * 2, lambda b: b * 3, lambda c: c * 4]
print(f7[0](6), f7[1](7), f7[2](8))  # 12 21 32

'''
eval()函数
功能：将字符串 str 当成有效的表达式来求值并返回计算结果。
语法： eval(source[, globals[, locals]]) -> value
参数:
    source：一个 Python 表达式或函数 compile()返回的代码对象
    globals：可选。必须是 dictionary
    locals：可选。任意映射对象
'''
print("eval()函数 test: ")
s = "print('abcde')"
eval(s)  # abcde

a = 20
b = 30
c = eval("a +b")
print(c)  # 50

'''
嵌套函数(内部函数)
嵌套函数：在函数内部定义的函数！
一般在什么情况下使用嵌套函数？
    1. 封装 - 数据隐藏：外部无法访问“嵌套函数”。
    2. 贯彻 DRY(Don’t Repeat Yourself) 原则：嵌套函数，可以让我们在函数内部避免重复代码。
    3. 闭包：后面会详细讲解。

'''
print("嵌套函数(内部函数) test:")


def printChineseName(name, familyName):
    print("{0} {1}".format(familyName, name))


def printEnglishName(name, familyName):
    print("{0} {1}".format(name, familyName))


# 使用 1个函数代替上面的两个函数
def printName(isChinese, name, familyName):
    def inner_print(a, b):
        print("{0} {1}".format(a, b))

    if isChinese:
        inner_print(familyName, name)
    else:
        inner_print(name, familyName)


printName(True, "小七", "高")
printName(False, "George", "Bush")

'''
nonlocal 关键字 
nonlocal 用来声明外层的局部变量。
global 用来声明全局变量。
'''
#
print("global nonlocal 关键字  test:")


def outer():
    b = 10

    def inner():
        nonlocal b  # 声名外部函数的局部变量
        print("inner b = " + str(b))
        b = 100

        global CONSTANT_A  # 声名全局变量
        CONSTANT_A = 999

    inner()
    print("outer b = " + str(b))


outer()
print("a = " + str(b))

'''
Python 在查找“名称”时，是按照 LEGB 规则查找的：Local-->Enclosed-->Global-->Built in
    Local 指的就是函数或者类的方法内部
    Enclosed 指的是嵌套函数（一个函数包裹另一个函数，闭包）
    Global 指的是模块中的全局变量
    Built in 指的是 Python 为自己保留的特殊名称。
如果某个 name 映射在局部(local)命名空间中没有找到，接下来就会在闭包作用域(enclosed)进行搜索，如果闭包作用域也没有找到，Python 就会到全局(global)命名空间中进行查找，
最后会在内建(built-in)命名空间搜索 （如果一个名称在所有命名空间中都没有找到，就会产生一个 NameError）。
'''



"""
装饰器
在代码运行期间，可以动态增加函数功能的方式，被称为装饰器【Decorator】 通过闭包函数实现
也就是说，在不修改原函数的基础上，给原函数增加功能
好处：在团队开发中，如果两个或者两个以上的程序员会用到相同的功能，但是功能又有细微的差别，采用装饰器：相互不影响，代码简化

注意:
1.在使用装饰器的简写方式的时候,原函数必须在装饰器函数的下面
2.outer就是装饰器函数.  @outer等价于  test = outer(test)
"""

# 系统的简写
# a.书写闭包函数    此处的outer函数就是装饰器函数
def outer(fn):  # b. fn表示形参,  实际调用的时候传递的是原函数的名字
    def inner():
        fn()  # c.调用原函数
        # d. 给原函数添加功能,   注意:添加的功能可以写在原函数的上面也可以写在原函数的下面

    print("我很好")
    return inner


# test = outer(test)

# 装饰器的简写方式 @ + 装饰器名称
@outer  # 等价于  =====>test = outer(test)
def test():
    print("你好啊!")


test()

# 不定长参数的装饰器(通用装饰器)
# 同一个装饰器装饰多个函数
def jisuan(fn):
    def inner(*args):
        print("数学运算的结果是:", end=" ")
        fn(*args)

    return inner


@jisuan
def add(a, b):
    print(a + b)


add(12, 34)


@jisuan
def cha(a, b, c):
    print(a - b - c)


cha(100, 23, 26)