# encoding: utf-8

# TODO traceback
import traceback

"""
traceback traceback模块提供了处理异常和调试的工具。它可以用于获取当前调用栈的信息，并且可以让开发者追踪到程序出现异常时的堆栈跟踪信息。
以下是traceback模块中一些常用的函数和方法：

1. print_tb(tb, limit=None, file=None)  打印当前调用栈的信息，其中tb是一个traceback对象，limit指定打印堆栈的深度，file指定输出堆栈信息的文件对象。
2. print_exc(limit=None, file=None)  打印当前异常的堆栈跟踪信息，limit指定打印堆栈的深度，file指定输出堆栈信息的文件对象。
3. format_tb(tb, limit=None)  返回当前调用栈的信息，以字符串列表的形式返回，tb是一个traceback对象，limit指定打印堆栈的深度。
4. format_exception(etype, value, tb, limit=None)  返回异常的堆栈跟踪信息，以字符串列表的形式返回，etype是异常类型，value是异常的值，tb是一个traceback对象，limit指定打印堆栈的深度。
5. extract_tb(tb, limit=None)  从traceback对象中提取堆栈跟踪信息，以元组的形式返回文件名、行号、函数名和源代码的文本行。limit指定提取堆栈的深度
"""


def demo():
    try:
        # 触发一个异常
        raise ValueError("An error occurred")
    except ValueError:
        # 捕获异常并打印追踪信息
        traceback.print_exc()


def foo():
    bar()


def bar():
    raise Exception("Oops, something went wrong")


if __name__ == '__main__':
    try:
        foo()
    except:
        # 1.
        traceback.print_exc()

        # 2.
        # traceback_str = traceback.format_exc()
        # print(traceback_str)