# encoding: utf-8

from io import StringIO

"""
StringIO是Python标准库中的一个模块，用于在内存中模拟文件的读写操作。它提供了一个类似文件对象的接口，允许你将字符串作为文件来读取和写入，而不需要实际创建物理文件。

StringIO模块中的主要类是StringIO.StringIO，在Python 2中，可以直接使用该类。但在Python 3中，它被移到了io模块中，因此需要使用io.StringIO。

下面是StringIO的一些常用方法：
io.StringIO([initial_value[, newline='\n']])：构造函数用于创建一个StringIO对象。initial_value是可选参数，用于指定初始字符串值，默认为空字符串。newline用于指定换行符，默认为\n。

getvalue()：获取StringIO对象当前包含的全部字符串值。
write(s)：将字符串s写入StringIO对象。
read(size=-1)：从StringIO对象读取size个字符，并返回读取的内容。如果size为负数或省略，则读取全部内容。
seek(offset[, whence])：移动文件指针到指定的位置。offset是偏移量，指定相对于whence的位置，默认为0。whence是可选参数，指定偏移量的基准位置，默认为0（文件的开头）。
close()  关闭流

使用场景：StringIO在需要使用文件对象进行读写操作时，但又不希望创建实际的物理文件时非常有用。它可以帮助你在内存中处理字符串数据，使得读写操作更加高效。
"""

# 1. 创建StringIO对象 StringIO()
string_io = StringIO()

# 2. 写入数据 write()
string_io.write("Hello, World!\n")
string_io.write("This is a test string.\n")

# 3.  将文件指针移动到文件开头 seek(0)
string_io.seek(0)

# 4. 将StringIO对象的内容读取并输出
print(string_io.read())

# 5. 获取StringIO对象的全部内容  getvalue()
print("全部内容：", string_io.getvalue())

# 6. 关闭StringIO对象
string_io.close()