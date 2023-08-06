# encoding: utf-8

import _thread
import time

"""

在Python程序中，可以通过“_thread”和threading（推荐使用）这两个模块来处理线程。在Python3中，thread模块已经废弃。可以使用threading模块代替。
所以，在Python3中不能再使用thread模块，但是为了兼容Python3以前的程序，在Python3中将thread模块重命名为“_thread”。

_thread 

创建:  t = _thread.start_new_thread(function, args[, kwargs])

"""


def fun():
    print('开始运行fun')
    time.sleep(2)
    print('运行fun2结束')


if __name__ == '__main__':
    print('开始运行')
    # 启动一个线程运行函数fun
    _thread.start_new_thread(fun, ())

    # 启动一个线程运行函数fun
    _thread.start_new_thread(fun, ())
    time.sleep(6)
