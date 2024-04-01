# encoding: utf-8

import inspect


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


if __name__ == '__main__':
    # configparser_test()
    # configparser_test2()

    inspect_test()
    # create_obj()