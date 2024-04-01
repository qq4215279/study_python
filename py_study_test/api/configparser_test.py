# encoding: utf-8

import configparser

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
