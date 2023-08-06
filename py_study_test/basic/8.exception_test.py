#  encoding: utf-8

import traceback
import os

"""
异常和错误
格式:
    try... 一个 except 结构
    
    try... 多个 except 结构
    
    try...except...else 结构
        增加了“else 块”。如果 try 块中没有抛出异常，则执行 else 块。如果try 块中抛出异常，则执行 except 块，不执行 else 块。
    
    try...except...finally 结构
        finally 块无论是否发生异常都会被执行；通常用来释放 try 块中申请的资源。

自定义异常类
自定义异常类一般都是运行时异常，通常继承 Exception 或其子类即可。命名一般以 Error、Exception 为后缀。
自定义异常由 raise 语句主动抛出。


trackback 模块
提供了有关异常（错误）的堆栈跟踪信息，可以帮助你追踪程序中发生的异常并找到异常的来源。堆栈跟踪信息包括了异常发生的文件、行号、函数调用栈等相关信息。
常用api:
    traceback.format_exc([limit[, chain]])  返回一个字符串，包含了当前异常的堆栈跟踪信息。可选参数 limit 控制跟踪的深度。
    traceback.format_exception(etype, value, tb[, limit[, chain]])  返回一个字符串列表，表示指定异常类型、异常值和堆栈跟踪信息的格式化输出。可选参数 limit 控制跟踪的深度。
    traceback.print_exc([limit[, api2]])  打印当前异常的堆栈跟踪信息到标准错误流（默认为 sys.stderr）。
    traceback.print_exception(etype, value, tb[, limit[, api2]])  打印指定异常类型、异常值和堆栈跟踪信息的格式化输出到指定文件流（默认为 sys.stderr）。可选参数 limit 控制跟踪的深度。
    traceback.print_last([limit[, api2]])  打印最近的异常信息。
    traceback.print_list(extracted_list[, api2])  打印通过 extract_tb() 或 extract_stack() 获取的堆栈跟踪信息。
    traceback.extract_tb(tb[, limit])  返回一个列表，包含从堆栈跟踪对象 tb 提取的堆栈帧信息。
    traceback.extract_stack([f[, limit]])  返回一个列表，包含当前堆栈的堆栈帧信息。

"""

"""
常见异常汇总
- ArithmeticError 所有数值计算错误的基类
- AssertionError 断言语句失败
- AttributeError 对象没有这个属性
- BaseException 所有异常的基类
- DeprecationWarning 关于被弃用的特征的警告
- EnvironmentError 操作系统错误的基类
- EOFError 没有内建输入,到达 EOF 标记
- Exception 常规错误的基类
- FloatingPointError 浮点计算错误
- FutureWarning 关于构造将来语义会有改变的警告
- GeneratorExit 生成器(generator)发生异常来通知退出
- ImportError 导入模块/对象失败
- IndentationError 缩进错误
- IndexError 序列中没有此索引(index)
- IOError 输入/输出操作失败
- KeyboardInterrupt 用户中断执行(通常是输入^C)
- KeyError 映射中没有这个键
- LookupError 无效数据查询的基类
- MemoryError 内存溢出错误(对于 Python 解释器不是致命的)
- NameError 未声明/初始化对象 (没有属性)
- NotImplementedError 尚未实现的方法
- OSError 操作系统错误
- OverflowError 数值运算超出最大限制
- OverflowWarning 旧的关于自动提升为长整型(long)的警告
- PendingDeprecationWarning 关于特性将会被废弃的警告
- ReferenceError 弱引用(Weak reference)试图访问已经垃圾回收了的对象
- RuntimeError 一般的运行时错误
- RuntimeWarning 可疑的运行时行为(runtime behavior)的警告
- StandardError 所有的内建标准异常的基类
- StopIteration 迭代器没有更多的值
- SyntaxError Python 语法错误
- SyntaxWarning 可疑的语法的警告
- SystemError 一般的解释器系统错误
- SystemExit 解释器请求退出
- TabError Tab 和空格混用
- TypeError 对类型无效的操作
- UnboundLocalError 访问未初始化的本地变量
- UnicodeDecodeError Unicode 解码时的错误
- UnicodeEncodeError Unicode 编码时错误
- UnicodeError Unicode 相关的错误
- UnicodeTranslateError Unicode 转换时错误
- UserWarning 用户代码生成的警告
- ValueError 传入无效的参数
- Warning 警告的基类
- WindowsError 系统调用失败
- ZeroDivisionError 除(或取模)零 (所有数据类型)
"""

"""
测试自定义异常类
"""


class AgeError(Exception):  # 继承 Exception
    def __init__(self, errorInfo):
        Exception.__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return str(self.errorInfo) + ",年龄错误！应该在 1-150 之间"


def custom_exception_test():
    # 如果为 True，则模块是作为独立文件运行，可以执行测试代码
    age = int(input("输入一个年龄:"))
    if age < 1 or age > 150:
        raise AgeError(age)
    else:
        print("正常的年龄：", age)


custom_exception_test()


def test_1():
    try:
        print("step1")
        a = 3 / 0
        print("step2")
    except BaseException as e:
        print("step3")
        print(e)
        traceback.print_exc()

        if not os.path.exists("file"):
            os.makedirs("file")

        path = r"D:\Code\PythonWorkSpace\study_python\py_study_test\basic\file\a.log"
        with open(path, "a+") as f:
            traceback.print_exc(file=f)
    print("step4")


test_1()


def test_2():
    try:
        a = input("请输入被除数：")
        b = input("请输入除数：")
        c = float(a) / float(b)
        print(c)
    except ZeroDivisionError:
        print("异常：除数不能为 0")
    except TypeError:
        print("异常：除数和被除数都应该为数值类型")
    except NameError:
        print("异常：变量不存在")
    except BaseException as e:
        print(e)
        print(type(e))


def test_3():
    try:
        a = input("请输入被除数：")
        b = input("请输入除数：")
        c = float(a) / float(b)
    except BaseException as e:
        print(e)
    else:
        print("除的结果是：", c)


def test_4():
    try:
        a = input("请输入一个被除数：")
        b = input("请输入一个除数：")
        c = float(a) / float(b)
    except BaseException as e:
        print(e)
    else:
        print(c)
    finally:
        print("我是 finally 中的语句，无论发生异常与否，都执行！")
    print("程序结束！")
