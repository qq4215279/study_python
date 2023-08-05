# encoding: utf-8

import zlib

"""
zlib是Python标准库中的一个模块，用于提供数据的压缩和解压缩功能。zlib模块在处理网络传输、文件压缩和加速数据传输等方面非常有用，可以帮助你优化数据传输和存储。

zlib模块的主要函数有：

zlib.compress(data, level=-1)  对数据进行压缩，data是要压缩的数据，level是压缩级别，取值范围是0（无压缩）到9（最大压缩）。默认值是-1，表示使用默认压缩级别。
zlib.decompress(data)  对压缩的数据进行解压缩，data是要解压缩的数据。

"""

# 原始数据
data = b"Hello, World! This is some data that needs to be compressed."

# 压缩数据 compress()
compressed_data = zlib.compress(data)

# 解压缩数据 decompress()
decompressed_data = zlib.decompress(compressed_data)

print("原始数据长度：", len(data))
print("压缩后数据长度：", len(compressed_data))
print("解压缩后数据：", decompressed_data)

# 错误处理  zlib异常: zlib.error
def error_test():
    # 无效的压缩数据
    invalid_compressed_data = b"This is not valid compressed data"

    try:
        decompressed_data = zlib.decompress(invalid_compressed_data)
    except zlib.error:
        print("Invalid compressed data")