# encoding: utf-8

import struct

"""
struct是Python标准库中的一个模块，用于处理二进制数据和C结构体的转换。它提供了一组函数，可以在Python中进行字节与数据类型之间的转换。
struct模块通常用于处理与底层操作相关的二进制数据，例如网络编程、文件IO、位操作等。

主要的struct模块函数包括：
struct.pack(format, v1, v2, ...)：将指定的Python值按照指定的格式（format）打包为一个二进制字符串（bytes对象）。格式后面的值只能与格式一致，否则会引发struct.error。。
       format是一个字符串，用于指定打包的格式。v1, v2, ...是要打包的值。常用的格式字符如下：
            b：有符号字节(char)
            B：无符号字节(unsigned char)
            c：字符
            d: 浮点数(double)
            f：浮点数(float)
            h：短整数（short)
            H：无符号短整数(unsigned short)
            i：整数(int)
            I：无符号整数(int)
            l：长整数(long)
            L：无符号长整数(unsigned long)
            q：长长整数(long long)
            Q：无符号长长整数(unsigned long long)
            s：字符串
            x: 填充字节
            ?: bool
            
struct.unpack(format, buffer)：根据指定的格式（format），从二进制字符串（buffer）中解析出相应的Python值，并以元组形式返回。
struct.calcsize(format)：返回给定格式（format）的结构的大小，即打包后的字符串长度。
"""

# 定义数据格式s
format_string = 'i 3s f'  # i: int, 2s: 2-byte string, f: float

# 打包数据
# packed_data = struct.pack(format_string, 42, b'jjhki', 3.14)
format_string = str(3) + "s" + str(2) + "s" + "i"
packed_data = struct.pack(format_string, "lll".encode(), b'jj', 3)

print("打包后的数据：", packed_data)

# 解析数据
unpacked_data = struct.unpack(format_string, packed_data)

print("解析后的数据：", unpacked_data)

print(unpacked_data[0])
print(unpacked_data[0].decode())

