# encoding: utf-8
import io

"""
一、字符串常用api
eg: str = " 我爱编程，我喜欢写代码，学习python很快乐，高兴，666，哈哈哈！！"
1. 字符串base操作：
    str(x) 将任意类型的x转化为字符串类型
    bytes(str, encoding='utf-8') 创建字节(bytes)字符串 eg: bytesStr = bytes("Hello, World!", encoding='utf-8')
    input() 从控制台读取字符串
    len(str) 返回字符串的长度。
    chr(x) 返回Unicode编码为x的字符
    ord(str) 字符串的Unicode编码
    oct(x) 将整数x转化为八进制数
    hex(x) 将整数x转化为十六进制数
    +：字符串拼接，将两个字符串连接起来。eg: str1 + str2
    *：字符串复制，将字符串重复多次。eg: str * n

2. 字符串切片：str[start : end : step] 切片操作，提取字符串的子串，从start索引（包含）到end索引（不包含），step不填，默认步长为1。
    str1[n] 使用[]提取字符
    str[起始偏移量start : 终止偏移量end : 步长step] 字符串切片slice操作
        [:] 提取整个字符串                                       "abcdef"[:]     =>  "abcdef"
        [start:]从 start 索引开始到结尾                          "abcdef"[2:]    =>  "cdef"
        [:end]从头开始知道 end-1                                 "abcdef"[:2]    =>  "ab"
        [start:end:step]从 start 提取到end-1，步长是 step        "abcdef"[1:5:2] =>  "bd"

4. 查找和替换：
    str.len()：返回字符串的长度。
    str.count("编程")  指定字符串出现了几次
    str.find(substring) 查找子字符串在字符串中的索引，如果找不到返回-1。
    str.rfind('高')  最后一次出现指定字符串的位置
    str.index(substring) 查找子字符串在字符串中的索引，如果找不到会引发异常。

4. 大小写转换和检查：
    str.lower() 产生新的字符串，将字符串转换为小写。
    str.upper() 产生新的字符串，将字符串转换为大写。
    str.swapcase() 产生新的字符串，所有字母大小写转换
    str.capitalize() 产生新的字符串，将字符串的首字母转换为大写，其他字母转换为小写。
    str.title() 产生新的字符串，将每个单词的首字母都转换为大写。

5. 替换、分割和连接：
    str.replace(old, new) 字符串替换
    str.split(separator) 分割，将字符串分割为子字符串列表，根据指定的分隔符。
    str.join(iterable) 合并，将可迭代对象中的字符串连接起来，用当前字符串作为分隔符。

6. 去除空白字符：
    str.strip() 去除字符串开头和结尾的空白字符。
    str.lstrip() 去除字符串开头的空白字符。
    str.rstrip() 去除字符串结尾的空白字符。

7. 判断字符串的内容：
    str.startswith(prefix) 检查字符串是否以指定前缀开头。
    str.endswith(suffix) 检查字符串是否以指定后缀结尾。
    str.islower() 检查字符串是否全为小写。
    str.isupper() 检查字符串是否全为大写。
    str.istitle() 检查字符串是否符合标题格式。
    str.isalnum() 是否全为字母或数字
    str.isalpha() 检测字符串是否只由字母组成(含汉字)。
    str.isdigit() 检测字符串是否只由数字组成。
    str.isnumeric() 检查字符串是否只包含数字（包括Unicode数字）。
    str.isspace() 检测是否为空白符
    str.isdecimal() 检查字符串是否只包含十进制字符。
    str.isascii() 检查字符串是否只包含ASCII字符。

8. 对齐和填充(用于对字符串实现排版)：
    str.center(width[, fillchar]) 将字符串居中，并使用指定字符（默认为空格）填充至指定的宽度。
    str.ljust(width[, fillchar]) 将字符串左对齐，并使用指定字符（默认为空格）填充至指定的宽度。
    str.rjust(width[, fillchar]) 将字符串右对齐，并使用指定字符（默认为空格）填充至指定的宽度.
    str.zfill(width) 将字符串填充为指定宽度，右对齐，不足的左边用0填充。

"""
# 字符串的编码
binaryA = ord('A')
print(binaryA)
binaryLiu = ord("刘")
print(binaryLiu)

# myName = input("请输入你的名字：")
# print(myName)
# print(len(myName))

# 字符串拼接
str1 = "a" + "b"
str2 = str1 * 3
print(str1)
print(str2)
print(str2[1])

# 4. index 找不到子串跑异常
indexStr = "liuzhen"
# print("index test: ", indexStr.index("刘"))


# 字符串切片slice操作
def sliceTest():
    print("abcdefghijklmnopqrstuvwxyz"[-3:])  # 倒数三个 xyz
    print("abcdefghijklmnopqrstuvwxyz"[-8:-3])  # 倒数第八个到倒数第三个(包头不包尾) stuvw
    print("abcdefghijklmnopqrstuvwxyz"[::-1])  # 步长为负，从右到左反向提取 zyxwvutsrqponmlkjihgfedcba


sliceTest()

# 字符串替换
str1 = "abadaa"
str1 = str1.replace("a", "振")
print(str1)

# split()分割
a = "你好 哈哈 刘振 name"
b = a.split(" ")  # ['你好', '哈哈', '刘振', 'name']
print(b)

# join() 合并
c = "*".join(b)  # 你好*哈哈*刘振*name
print(c)

# 格式排版 center() ljust() rjust()
a = "LIU"
b = a.center(13, "&")
print(b)  # "&&&&&LIU&&&&&"
b = a.center(13)
print(b)  # "      LIU     "
b = a.ljust(13, "*")
print(b)  # "LIU**********"

# 可变字符串: 在 Python 中，字符串属于不可变对象，不支持原地修改，如果需要修改其中的值，智能创建新的字符串对象。但是，经常我们确实需要原地修改字符串，可以使用 io.StringIO 对象或 array 模块。
s = "hello,sxt"
sio = io.StringIO(s)
value = sio.getvalue()
print("value: " + value)  # hello,sxt
seek = sio.seek(7)
print("seek: " + str(seek))  # 7  （下一步write将操作x）
sio.write('g')  # 将 x 变为 g
value = sio.getvalue()
print("value2: " + value)  # hello,sgt

"""
二、格式化字符串：str.format() 基本语法是通过 {} 和 : 来代替以前的 % 。format 函数可以接受不限个参数，位置可以不按顺序。eg:
    - 填充与对齐：填充常跟对齐一起使用
            "^"、"<"、">" 分别是居中、左对齐、右对齐，后面带宽度
            : 号后面带填充的字符，只能是一个字符，不指定的话默认是用空格填充
    - 数字格式化：浮点数通过 f，整数通过 d 进行需要的格式化。
    - 可变字符串：在 Python 中，字符串属于不可变对象，不支持原地修改，如果需要修改其中的值，智能创建新的字符串对象。但是，经常我们确实需要原地修改字符串，
        可以使用 io.StringIO 对象或 array 模块。
"""


def formatStrTest():
    # 1. 在字符串中使用占位符 {} 来指示要插入的位置。然后，通过 format() 方法将值传递给这些占位符，以替换它们
    name = "Alice"
    age = 30
    message1 = "My name is {} and I am {} years old.".format(name, age)
    print("message1: ", message1)

    # 2. 按位置插入：可以通过位置参数将值插入到占位符中。
    message2 = "My name is {0} and I am {1} years old. {0} very great!".format(name, age)
    print("message2: ", message2)

    # 3. 按关键字插入：可以使用关键字参数将值插入到占位符中。
    message3 = "My name is {name} and I am {age} years old".format(name=name, age=age)
    print("message3: ", message3)

    # 4. 格式规范和位置参数结合：可以将格式规范和位置参数结合使用。
    data = ("Alice", 30)
    message5 = "My name is {0[0]} and I am {0[1]} years old.".format(data)
    print("message5: ", message5)

    # 5. f-strings（Python 3.6+）：f-strings 是一种更简洁的字符串格式化方法，可以在字符串前加上 f，然后在字符串中使用花括号插入变量。
    message6 = f"My name is {name} and I am {age} years old."
    print("message6: ", message6)

    # 6.1 数字格式化 格式规范：在占位符内部，可以使用格式规范来控制插入值的显示方式，如小数位数、对齐、填充等。
    pi = 3.141592653589793
    # 保留两位小数
    print("formatted_pi: ", "Value of pi: {:.2f}".format(pi))
    print("我是{0}，我的村快有{1:.2f}".format("刘振", 10000.9999))  # 我是刘振，我的村快有10001.00
    print("{:=^30.4f}".format(pi))  # ============3.1416============

    # 6.2 填充与对齐
    # 6.2.1 居中
    print("{:*^10}".format("Mike"))  # ***Mike***
    # 6.2.2 左对齐
    print("{:*<10}".format("Mike"))  # Mike******
    # 6.2.3 右对齐
    print("{:*>10}".format("Mike"))  # ******Mike
    print("{:>8}".format("256"))  # "     256"


formatStrTest()

"""
三、字符串编码和解码：
bytesStr = str.encode(encoding='utf-8') 将字符串编码为指定字符编码的字节序列。
newStr = bytes.decode(encoding='utf-8') 将字节序列解码为字符串，使用指定字符编码。

Python支持两种类型的字符串：Unicode字符串和字节字符串。
- Unicode字符串：以普通字符串的形式表示文本，可以包含各种字符和编码，通常用于处理文本数据和字符处理。定义Unicode字符串时，不需要在字符串前面加上b。
- 字节字符串（bytes对象）：以字节的形式表示二进制数据，通常用于处理和传输二进制数据，例如网络通信、文件读写、加密等。定义字节字符串时，需要在字符串前面加上b。

创建字节(bytes)字符串:
"""


def createBytesStr():
    # 1. bytes()
    bytesStr = bytes("Hello, World!", encoding='utf-8')
    print("字节字符串类型：", type(bytesStr))  # <class 'bytes'>

    # 2.1. encode()
    text_str = "Hello, World!"
    bytesStr = text_str.encode('utf-8')
    print("字节字符串类型：", type(bytesStr))  # <class 'bytes'>

    # 2.2. decode()
    new_text_str = bytesStr.decode(encoding='utf-8')
    print("原字符串：", new_text_str, " 字节字符串类型：", type(new_text_str))

    # 3. b"str"  只需在字符串前加上b。
    bytesStr = b"Hello, World!"
    print("字节字符串类型：", type(bytesStr))  # <class 'bytes'>

    # 普通字符串
    print("普通字符串类型：", type("Hello, World!"))  # <class 'str'>


createBytesStr()

"""
四、特殊字符串
1. 在字符串前面加上 r 表示原始字符串（Raw String），它的作用是告诉Python解释器不对字符串中的转义字符进行特殊处理，而是将字符串内容按照字面意义来使用。
2. 在字符串前面加上 b ，表示生成字节字符串
3. 在字符串前面加上 f ，表示对字符串进行格式化。
"""


def specialStr():
    # 1. r""
    normal_string = "Hello\nWorld"
    print("normal_string: ", normal_string)
    rStr = r"Hello\nWorld"
    print("rStr: ", rStr)

    # 2. b""
    bStr = b"Hello World"
    print("bStr type: ", type(bStr))  # bStr type:  <class 'bytes'>

    # 3. f""
    name = "lihua"
    fStr = f"My name is {name}"
    print("fStr: ", fStr)


specialStr()
