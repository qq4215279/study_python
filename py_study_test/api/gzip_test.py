# encoding: utf-8

import gzip

"""
gzip模块 用于对数据进行压缩和解压缩。它是基于DEFLATE压缩算法的实现，类似于zlib模块，但在处理压缩文件时更常用。

gzip模块主要提供了gzip.GzipFile类来处理压缩文件，同时也有一些方便的函数用于直接压缩和解压缩数据。


1. gzip.compress(data, compresslevel=9)：该函数用于对数据进行压缩。
        data 是要压缩的数据，一个字节字符串（bytes对象）
        compresslevel 是压缩级别，取值范围是0（无压缩）到9（最大压缩）。默认值是9，表示使用最大压缩级别。

2. gzip.decompress(data)：该函数用于对压缩的数据进行解压缩。data是要解压缩的数据，必须是一个字节字符串（bytes对象）。

3. gzip.open(filename, mode='rb', compresslevel=9, encoding=None, errors=None, newline=None) 这是一个类似于内置的open()函数的函数，用于打开压缩的文件并返回一个文件对象。
        filename是要打开的文件名，mode是打开文件的模式
        compresslevel是压缩级别，取值范围是0（无压缩）到9（最大压缩）。默认值是9，表示使用最大压缩级别。    
   注意，我们需要使用二进制模式('wb'和'rb')来打开gzip文件。这是因为gzip文件包含二进制数据，而不是文本数据。    
"""

data = b"Hello, World! This is some data that needs to be compressed."
# 1. 压缩 compress()
compressed_data = gzip.compress(data, compresslevel=9)
print(compressed_data)

# 2. 解压
decompressed_data = gzip.decompress(compressed_data)
print(decompressed_data)

# 3. gzip模块提供了GzipFile类，我们可以使用这个类的write()和read()方法，分别对gzip文件进行写入和读取。
# 3.1 创建一个新的 gzip 文件，并写入数据
with gzip.open('./file/data.txt.gz', 'wb') as f:
    f.write(b"Hello, World! This is some data that needs to be compressed.")

# 3.2 读取 gzip 文件中的数据
with gzip.open('./file/data.txt.gz', 'rb') as f:
    file_content = f.read()

print(f"File content: {file_content}")