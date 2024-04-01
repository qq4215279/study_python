# encoding: utf-8

import time

"""
time 是 Python 标准库中用于处理时间的模块之一。它提供了许多函数来获取当前时间、操作时间对象以及进行时间格式化等操作。

常用api:
1. time.time(): 返回当前时间的时间戳，带小数点的秒数。
    转整形秒数: int(time.time())
    转毫秒值: int(time.time() * 1000)
2. time.localtime(): 返回当前时间的结构化时间对象，表示本地时间。
3. time.gmtime(): 返回当前时间的结构化时间对象，表示UTC时间（世界标准时间）。
4. time.strftime(format, t): 将结构化时间对象格式化为指定的字符串表示，其中 format 是格式化字符串，t 是结构化时间对象。
5. time.sleep(secs): 暂停程序执行指定秒数。
6. time.mktime(t): 将结构化时间对象转换为时间戳。
7. time.strptime(string, format): 将字符串解析为结构化时间对象，其中 string 是时间字符串，format 是字符串的格式。

8. time.clock(): 返回当前程序的CPU执行时间。
9. time.process_time(): 返回当前程序的系统CPU执行时间。
"""

if __name__ == '__main__':
    # 1.1.  获取当前时间戳
    timestamp = time.time()
    print("Current timestamp:", timestamp)
    # 1.2. 整秒
    seconds = int(time.time())
    print(seconds)
    # 1.3. 获取当前时间的毫秒值
    millSeconds = int(time.time() * 1000)
    print(millSeconds)

    # 2. 获取本地时间
    local_time = time.localtime(timestamp)
    # 4. 格式化当前时间
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    print("Formatted local time:", formatted_time)
