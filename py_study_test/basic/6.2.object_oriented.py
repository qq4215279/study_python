# encoding: utf-8

import copy

'''
面向对象
'''

'''
Python 支持多重继承，一个子类可以继承多个父类。
Python 支持多重继承，一个子类可以有多个“直接父类”。这样，就具备了“多个父类”的特点。但是由于，这样会被“类的整体层次”搞的异常复杂，尽量避免使用。
继承的语法格式如下：
    class 子类类名(父类 1[，父类 2，...]):
	    类体
	
类成员的继承和重写:
    1. 成员继承：子类继承了父类除构造方法之外的所有成员。
    2. 方法重写：子类可以重新定义父类中的方法，这样就会覆盖父类的方法，也称为“重写”	
'''

'''
api：
类方法: Class.mro() 或 类的属性: obj.__mro__ : 查看类的继承的层次结构
obj.dir()  查看对象属性
obj.__str__()  用于返回一个对于“对象的描述”，对应于内置函数 str() 经常用于 print()方法，帮助我们查看对象的信息。__str__()可以重写。

'''

'''
多态
多态（polymorphism）是指同一个方法调用由于对象不同可能会产生不同的行为。在现实生活中，我们有很多例子。比如：同样是调用人的休息方法，张三的休息是睡觉，
李四的休息是玩游戏，高淇老师是敲代码。同样是吃饭的方法，中国人用筷子吃饭，英国人用刀叉吃饭，印度人用手吃饭。
关于多态要注意以下 2 点：
1. 多态是方法的多态，属性没有多态。
2. 多态的存在有 2 个必要条件：继承、方法重写。

组合
is-a 关系，我们可以使用“继承”。从而实现子类拥有的父类的方法和属性。“is-a” 关系指的是类似这样的关系：狗是动物，dog is animal。狗类就应该继承动物类。
has-a 关系，我们可以使用“组合”，也能实现一个类拥有另一个类的方法和属性。” has-a”关系指的是这样的关系：手机拥有 CPU。

对象的浅拷贝和深拷贝:
变量的赋值操作
只是形成两个变量，实际还是指向同一个对象。
浅拷贝:
Python 拷贝一般都是浅拷贝。拷贝时，对象包含的子对象内容不拷贝。因此，源对象 和拷贝对象会引用同一个子对象。
深拷贝:
使用 copy 模块的 deepcopy 函数，递归拷贝对象中包含的子对象。源对象和拷贝对象所有的子对象也不同。
'''
class Animal:
    def shout(self):
        print("动物叫了一声...")

class Dog(Animal):
    def shout(self):
        print("狗叫了一声...")

class Cat(Animal):
    def shout(self):
        print("猫叫了一声...")

def animalShout(animal):
    if isinstance(animal, Animal):
        animal.shout()

print("多态 开始 test ----->")
dog = Dog()
cat = Cat()
animalShout(dog)
animalShout(cat)

# 浅拷贝
dog2 = copy.copy(dog)
print("浅拷贝: ", dog, dog2)
# 深拷贝
cat2 = copy.deepcopy(cat)
print("深拷贝：", cat, cat2)

'''
 多重继承:
 Python 支持多重继承，一个子类可以有多个“直接父类”。这样，就具备了“多个父类”的特点。但是由于，这样会被“类的整体层次”搞的异常复杂，尽量避免使用。
'''
class A:
    def aa(self):
        print("aa")


class B:
    def bb(self):
        print("bb")


class C(B, A):
    def cc(self):
        print("cc")


print("类的多重继承 test --------->")
c = C()
c.cc()
c.bb()
c.aa()

'''
特殊方法：
| 方法               | 说明       | 例子                   |
| -------------------| ---------- | ---------------------- |
| __init__           | 构造方法   | 对象创建：p = Person() |
| __del__            | 析构方法   | 对象回收               |
| __repr__,__str__   | 打印，转换 | print(a)               |
| __call__           | 函数调用   | a()                    |
| __getattr__        | 点号运算   | a.xxx                  |
| __setattr__        | 属性赋值   | a.xxx = value          |
| __getitem__        | 索引运算   | a[key]                 |
| __setitem__        | 索引赋值   | a[key]=value           |
| __len__            | 长度       | len(a)                 |

特殊属性：
Python 对象中包含了很多双下划线开始和结束的属性，这些是特殊属性，有特殊用法。这里我们列出常见的特殊属性：
| 特殊方法               | 含义                   |
| ---------------------- | ---------------------  |
| obj.__dict__           | 对象的属性字典          |
| obj.__class__          | 对象所属的类            |
| class.__bases__        | 类的基类元组（多继承）  |
| class.__base__         | 类的基类               |
| class.__mro__          | 类层次结构             |
| class.__subclasses__() | 子类列表               |

重载运算符：
| 运算符   | 特殊方法                                          | 说明                               |
| -------- | ------------------------------------------------ | ---------------------------------- |
| 运算符+  | __add__                                           | 加法                               |
| 运算符-  | __sub__                                           | 减法                               |
| <,<=,==  | __lt__, __le__, __eq__                            | 比较运算符                         |
| >,>=,!=  | __gt__, __ge__, __ne__                            |                                    |
| \|,^,&   | __or__, __xor__, __and__                          | 或、异或、与                       |
| <<,>>    | __lshift__, __rshift__                            | 左移、右移                         |
| *,/,%,// | __mul__, __truediv__, __mod__, __floordiv__       | 乘、浮点除、模运算（取余）、整数除  |
| **       | __pow__                                           | 指数运算                           |
'''


"""
动态创建对象
如果你想要在运行时通过字符串类名动态创建对象，可以使用 globals() 或 locals() 函数来获取类对象。
"""
# 定义一个简单的类
class Person:
    def __init__(self, name=None, age=None, gender=None):
        self.name = name  # 实例属性 name
        self.age = age    # 实例属性 age
        self.gender = gender    # 实例属性 age

    def greet(self):
        return f"你好，我是 {self.name}，我 {self.age} 岁。"

    def update_age(self, new_age):
        self.age = new_age

    def __str__(self):
        return f"Person(name={self.name}, age={self.age}, gender={self.gender})"

def createOBAndSetValue():
    class_name = "Person"
    person_dict = {"name": "lihua", "sex": "男", "age": 100}

    # 从全局命名空间中获取类
    person = globals()[class_name]
    person = person()

    # 使用外部函数更新对象的属性
    update_attributes(person, person_dict)

    # 输出更新后的属性
    print(person)  # 输出: Person(name=小红, age=30, gender=男)

    # 调用方法的字符串名称
    method_name = "greet"

    # 使用 getattr() 调用指定名称的方法
    greeting_method = getattr(person, method_name)
    print(greeting_method())

    # 更新年龄的方法
    update_method_name = "update_age"
    new_age = 30

    # 使用 getattr() 调用指定名称的方法并传参
    update_method = getattr(person, update_method_name)
    update_method(new_age)  # 正确调用更新年龄的方法
    print(person)

def update_attributes(instance, attributes):
    """
    更新对象的属性。
    :param instance: 要更新的对象实例
    :param attributes: 包含属性名称及其新值的字典
    """
    for key, value in attributes.items():
        setattr(instance, key, value)
        # if hasattr(instance, key):
        #     setattr(instance, key, value)
        #     print(f"更新属性: {key} = {value}")
        # else:
        #     print(f"属性 {key} 不存在")


createOBAndSetValue()