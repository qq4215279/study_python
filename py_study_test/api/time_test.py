# encoding: utf-8

# TODO time
import sys
import time


if __name__ == '__main__':
    milliseconds = int(time.time())
    print(milliseconds)

    # 获取当前时间的毫秒值
    milliseconds = int(time.time() * 1000)
    print(milliseconds)

    print(sys.maxsize)