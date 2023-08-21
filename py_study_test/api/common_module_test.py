# encoding: utf-8

import random
import configparser
import inspect
# TODO traceback
import traceback
# TODO time
import time

"""
random 模块
random 模块是 Python 标准库中的一个模块，提供了生成随机数的功能。它可以用于生成随机数、随机选择元素、打乱序列等各种与随机性相关的操作。

api: 
    randint(a, b)  生成一个介于 a 和 b 之间的整数，包括 a 和 b。
    random()  生成一个0到1之间的随机浮点数。
    uniform(a, b)  生成一个在范围 a 到 b 之间的随机浮点数。
    choice(seq)  从序列 seq 中随机选择一个元素并返回。
    randrange(start, stop[, step])  生成一个在指定范围内的随机整数，start 是范围的起始值，stop 是范围的结束值（不包括在内），step 是步长。
    sample(population, k)  从 population 中随机选择 k 个不重复的元素，返回一个列表。
    shuffle(seq)  打乱序列 seq 中的元素的顺序，改变原始序列。
    
    seed(a=None)  初始化随机数生成器的种子。如果不提供 a，则使用系统时间作为种子。
    random.getrandbits(k)  生成 k 个随机的比特位，返回一个整数。
    random.expovariate(lambd)  生成一个指数分布的随机浮点数，参数 lambd 是指数分布的参数。
    random.gauss(mu, sigma)  生成一个服从高斯分布（正态分布）的随机浮点数，mu 是均值，sigma 是标准差。
    random.choices(population, weights=None, cum_weights=None, k=1)  从 population 中根据权重随机选择 k 个元素，返回一个列表。
    random.betavariate(alpha, beta)  生成一个贝塔分布的随机浮点数，参数 alpha 和 beta 是贝塔分布的参数。
    random.paretovariate(alpha)  生成一个帕累托分布的随机浮点数，参数 alpha 是分布的形状参数。    
"""
def random_test():
    print("范围整数: ", random.randint(1, 2))
    print("0-1随机浮点数: ", random.random())
    print("范围随机浮点数: ", random.uniform(1, 4))
    fruits = ['apple', 'banana', 'cherry', 'date']
    print("随机选择一个元素: ", random.choice(fruits))
    print("指定范围内的随机整数: ", random.randrange(1, 10, 2))
    print("随机选择 k 个不重复的元素: ", random.sample((1, 4, 55, 100, 999), 3))
    random.shuffle(fruits)
    print("打乱列表中的元素顺序: ", fruits)


"""
configparser 用于解析配置文件。

创建一个配置文件：创建一个文本文件，例如 config.ini，写入你的配置信息。配置文件的格式通常是 键 = 值
用于解析和操作配置文件。它支持读取、修改和写入配置文件，配置文件的格式通常是 .ini 或 .properties 格式，由一系列的键值对组成。

config = ConfigParser()  创建一个配置文件解析器对象。
api:
以下是一些常用的 configparser 模块方法和属性：
    read(filename)  从指定文件中读取配置信息。
    read_file(f)  从已打开的文件对象 f 中读取配置信息。
    sections()  返回配置文件中所有的节（sections）的名称。
    options(section)  返回指定节中所有配置项的名称。
    add_section(section)  添加sections节
    get(section, option)  获取指定节中指定配置项的值。
    set(section, option, value)  设置指定节中指定配置项的值。
    write(fileobject)  将配置信息写入一个文件对象。
    has_section(section)  检查是否存在指定名称的节。
    has_option(section, option)  检查是否存在指定节中指定配置项。
    remove_section(section)  删除指定的节。
    remove_option(section, option)  删除指定节中指定配置项。
    
使用分号 ; 或井号 # 开头来编写注释。任何位于分号或井号后面的内容都会被视为注释，不会被解析为配置项。    
"""
def configparser_test():
    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read('./file/config.ini', encoding='utf-8')

    # 遍历所有节
    for section in config.sections():
        print(f"Section: {section}")

        # 遍历当前节中的所有配置项
        for option in config.options(section):
            value = config.get(section, option)
            print(f" {option} = {value}")

    # 获取配置项的值
    print("Option 1:", config.get('Section1', 'option1'))

    # 修改配置项的值
    config.set('Section1', 'option2', 'new_value')

    if not config.has_section("NewSection"):
        config.add_section("NewSection")
    config.set("NewSection", "newOption", "bbb")


    # 将修改后的配置写回文件
    with open('./file/config.ini', 'w') as configfile:
        config.write(configfile)

# 解析 properties 后缀的配置文件。通过 read_file(file) 方法。读取后，其他api同上
def configparser_test2():
    # 创建一个 ConfigParser 对象
    config = configparser.ConfigParser()

    # 使用 read_file() 方法读取配置文件
    with open(r'./file/config.properties', encoding='utf-8') as f:
        config.read_file(f)

    # 获取配置项的值
    print("pption 1:", config.get('DEFAULT', 'option1'))


"""
反射
在 Python 中，反射主要涉及以下几个内置函数和机制：
    getattr(object, name[, default])  获取对象 object 的名为 name 的属性。如果属性不存在，可以通过 default 参数提供默认值。
    hasattr(object, name)  检查对象 object 是否有名为 name 的属性，如果有返回 True，否则返回 False。
    setattr(object, name, value)  设置对象 object 的名为 name 的属性为给定的 value。
    delattr(object, name)  删除对象 object 的名为 name 的属性。
    dir([object])  返回对象（或当前作用域内的所有对象）的属性列表。可以用于查看对象的可用属性。
    type(object)  返回对象 object 的类型。
    isinstance(object, classinfo)  检查对象 object 是否是给定类型 classinfo 的实例。
    字符串调用方法  使用字符串动态调用对象的方法，可以使用 getattr() 获取方法，然后通过 () 运算符调用。
"""
def reflect_test():
    pass

"""

inspect 模块来检查模块中的所有成员，并筛选出类对象。inspect 模块提供了许多有用的函数，用于检查各种对象的信息，包括模块、类和函数。
"""
def inspect_test():
    # TODO

    # 获取当前模块对象
    current_module = inspect.currentframe().f_globals['__name__']
    module = __import__(current_module)

    # 获取当前模块中的所有成员
    all_members = inspect.getmembers(module)

    # 筛选出类对象
    classes = [member[1] for member in all_members if inspect.isclass(member[1])]

    # 打印所有类的名称
    for cls in classes:
        print("Class:", cls.__name__)


def create_obj():
    # 方式1：
    # 获取类名
    class_name = "MyClass"

    # 根据类名获取类对象
    class_obj = globals()[class_name]

    # 使用类对象创建实例
    instance = class_obj("Hello")

    # 打印实例的属性
    print(instance.value)

    print("-------------------------->")

    # 方式2：
    # 获取当前模块对象
    current_module = inspect.currentframe().f_globals['__name__']
    module = __import__(current_module)
    # 获取类对象
    class_obj = getattr(module, class_name)

    # 使用类对象创建实例
    instance = class_obj("World")

    # 打印实例的属性
    print(instance.value)


class MyClass:
    def __init__(self, value):
        self.value = value


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

import struct
if __name__ == '__main__':
    # random_test()

    # configparser_test()
    # configparser_test2()

    # inspect_test()
    # create_obj()

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

    milliseconds = int(time.time())
    print(milliseconds)

    # 获取当前时间的毫秒值
    milliseconds = int(time.time() * 1000)
    print(milliseconds)



