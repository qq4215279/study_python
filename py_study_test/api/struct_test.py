# encoding: utf-8

import struct

"""
struct是Python标准库中的一个模块，用于处理二进制数据和C结构体的转换。它提供了一组函数，可以在Python中进行字节与数据类型之间的转换。
struct模块通常用于处理与底层操作相关的二进制数据，例如网络编程、文件IO、位操作等。

主要的struct模块函数包括：
struct.pack(format, v1, v2, ...)：将指定的Python值按照指定的格式（format）打包为一个二进制字符串（bytes对象）。格式后面的值只能与格式一致，否则会引发struct.error。。
       format是一个字符串，用于指定打包的格式。v1, v2, ...是要打包的值。常用的格式字符如下：
            ?: bool
            c：字符
            b：有符号字节(char)
            B：无符号字节(unsigned char)
            h：短整数（short)
            H：无符号短整数(unsigned short)
            i：整数(int)
            I：无符号整数(int)
            l：长整数(long)
            L：无符号长整数(unsigned long)
            q：长长整数(long long)
            Q：无符号长长整数(unsigned long long)
            f：浮点数(float)
            d: 浮点数(double)
            s：字符串
            x: 填充字节
            
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



"""
编码 int 类型
"""
def encode_int_2_bytes(size, num):
    if num is None:
        num = 0

    return num.to_bytes(size, "big")
    # if num >= 0:
    #     return num.to_bytes(size, "big")
    # else:
    #     return num.to_bytes(size, "big", True)

"""
读 int 类型
int.from_bytes() 是 Python 内置的一个方法，用于将字节序列（bytes）转换为整数。这在处理二进制数据时非常有用，特别是在网络通信、文件读写等领域。
该方法的使用方式是调用 int.from_bytes(bytes, byteorder, signed=False)，其中：
    bytes 是要转换的字节序列。
    byteorder 指定字节序列的字节顺序，可以是 'big'（大端序，高位在前）或 'little'（小端序，低位在前）。
    signed 是一个可选参数，用于指定是否将结果解释为有符号整数。默认为 False，即将结果解释为无符号整数。
"""
def decode_bytes_2_int(read_size, stream):
    byte_val = stream.read(read_size)
    value = int.from_bytes(byte_val, "big")
    return value

if __name__ == '__main__':
    size = 4
    num = 100

    bytesArr = struct.pack(">i", num)
    # print(encode_int_2_bytes(size, num))
    print("i: ", struct.pack("i", num))
    print(">i: ", struct.pack(">i", num))

    print("I: ", struct.pack("I", num))
    print(">I: ", struct.pack(">I", num))
    print(bin(100))

    print("----------->")
    print(">i: ", struct.unpack(">i", bytesArr))
    print(">i: ", struct.unpack(">i", b"\x00\x00\x00\x00"))

    print(">i: ", struct.unpack(">i", b'\x00\x00\x00\x00'))

    print(">i: ", struct.unpack(">i", b'\x7f\xd2\x00\x00'))
