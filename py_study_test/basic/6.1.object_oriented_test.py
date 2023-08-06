'''
面向对象
'''

'''
类的定义：
class 类名：
	类体
	
要点如下：
1. 类名必须符合“标识符”的规则；一般规定，首字母大写，多个单词使用“驼峰原则”。
2. 类体中我们可以定义属性和方法。
3. 属性用来描述数据，方法(即函数)用来描述这些数据相关的操作。	

实例方法：实例方法是从属于实例对象的方法。实例方法的定义格式如下：
def 方法名(self [, 形参列表])：
	函数体

方法的调用格式如下：对象.方法名([实参列表])
要点：
    1. 定义实例方法时，第一个参数必须为 self。和前面一样，self 指当前的实例对象。
    2. 调用实例方法时，不需要也不能给 self 传参。self 由解释器自动传参。

api：
__init__() 方法: 初始化创建好的对象，初始化指的是：“给实例属性赋值”
    如果我们不定义`__init__`方法，系统会提供一个默认的`__init__`方法。如果我们定义了带参 的`__init__`方法，系统不创建默认的`__init__`方法。
__new__() 方法: 用于创建对象，但我们一般无需重定义该方法。
__del__ 方法(析构函数): 称为“析构方法”，用于实现对象被销毁时所需的操作。比如：释放对象占用的资源，例如：打开的文件资源、网络连接等。
    Python 实现自动的垃圾回收，当对象没有被引用时（引用计数为 0），由垃圾回收器 调用`__del__`方法。
    我们也可以通过 del 语句删除对象，从而保证调用`__del__`方法。系统会自动提供`__del__`方法，一般不需要自定义析构方法。
__call__ 方法: 称为“可调用对象”，即该对象可以像函数一样被调用。    

属性和方法命名总结:
·_xxx：保护成员，不能用“from module import * ”导入，只有类对象和子类对象能访问这些成员。
·__xxx： 类中的私有成员，只有类对象自己能访问，子类对象也不能访问。（但在类外部可以通过“ 对象名._类名__xxx ”这种特殊方式访问。Python 不存在严格意义的私有成员）
·__xxx__：系统定义的特殊成员
注：再次强调，方法和属性都遵循上面的规则。

类编码风格:
1. 类名首字母大写，多个单词之间采用驼峰原则。
2. 实例名、模块名采用小写，多个单词之间采用下划线隔开。
3. 每个类，应紧跟“文档字符串”，说明这个类的作用。
4. 可以用空行组织代码，但不能滥用。在类中，使用一个空行隔开方法；模块中，使用两 个空行隔开多个类。
'''


class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def say_score(self):
        print(self.name, "的分数是：", self.score)


'''
1. 类对象  类定义格式中，“`class 类名: ”。实际上，当解释器执行 class 语句时，就会创建一个类对象。

2. 类属性  类属性是从属于“类对象”的属性，也称为“类变量”。由于，类属性从属于类对象，可以被所有实例对象共享。
    class 类名：
	    类变量名= 初始值  # 定义类属性
使用：通过：“类名.类变量名”来读写。

3. 类方法  类方法是从属于“类对象”的方法。类方法通过装饰器@classmethod 来定义
    @classmethod
    def 类方法名(cls [,形参列表]):
	    函数体
	    
要点如下：
    1. @classmethod 必须位于方法上面一行
    2. 第一个 cls 必须有；cls 指的就是“类对象”本身；
    3. 调用类方法格式：“`类名.类方法名(参数列表)`”。 参数列表中，不需要也不能给 cls 传值。
    4. 类方法中访问实例属性和实例方法会导致错误
    5. 子类继承父类方法时，传入 cls 是子类对象，而非父类对象  
  
4. 静态方法  Python 中允许定义与“类对象”无关的方法，称为“静态方法”。
“静态方法”和在模块中定义普通函数没有区别，只不过“静态方法”放到了“类的名字空 间里面”，需要通过“类调用”。
静态方法通过装饰器**@staticmethod** 来定义，格式如下：
    @staticmethod
    def 静态方法名([形参列表]):
	    函数体
	    
要点如下：
    1. @staticmethod 必须位于方法上面一行
    2. 调用静态方法格式：“`类名.静态方法名(参数列表)`”。
    3. 静态方法中访问实例属性和实例方法会导致错误	    
'''


class User:
    # 2. 类属性
    userName = "root"

    # 3. 类方法
    @classmethod
    def printUserName(cls):
        print("调用类方法：")
        print("用户名：", cls.userName)

    # 4. 静态方法
    @staticmethod
    def add(a, b):
        print("调用静态方法：")
        print("{0} + {1} = {2}".format(a, b, (a + b)))
        return a + b


user = User()
print("userName: ", user.userName)

User.printUserName()

User.add(10, 20)

'''
方法没有重载:
在其他语言中，可以定义多个重名的方法，只要保证方法签名唯一即可。方法签名包含 3个部分：`方法名`、`参数数量`、`参数类型`。
Python 中，方法的的参数没有声明类型（调用时确定参数的类型），参数的数量也可以由可变参数控制。因此，Python 中是没有方法的重载的。
定义一个方法即可有多种调用方式，相当于实现了其他语言中的方法的重载。如果我们在类体中定义了多个重名的方法，只有最后一个方法有效。
建议：不要使用重名的方法！Python 中方法没有重载。

方法的动态性:
Python 是动态语言，我们可以动态的为类添加新的方法，或者动态的修改类的已有的方法。

私有属性和私有方法(实现封装):
Python 对于类的成员没有严格的访问控制限制，这与其他面向对象语言有区别。关于私有属性和私有方法，有如下要点：
1. 通常我们约定，两个下划线开头的属性是私有的(private)。其他为公共的(public)。
2. 类内部可以访问私有属性(方法)
3. 类外部不能直接访问私有属性(方法)
4. 类外部可以通过“`obj._类名__私有属性(方法)名`”访问私有属性(方法)
【注】方法本质上也是属性！只不过是可以通过()执行而已。所以，此处讲的私有属性和公有属性，也同时讲解了私有方法和公有方法的用法。
如下测试中，同时也包含了私有方法和公有方法的例子。

@property 装饰器
@property 可以将一个方法的调用方式变成“属性调用”。下面是一个简单的示例，让大家体会一下这种转变：
@property 主要用于帮助我们处理属性的读操作、写操作。

'''

class Employee:

    # 定义私有属性 通过 dir 可以查到_Employee__company
    __company = "hario game"
    salary = 0

    """
    初始化创建好的对象，初始化指的是：“给实例属性赋值”
    """
    def __init__(self, name, age):
        self.name = name
        # 私有实例属性
        self.__age = age

    """
    用于返回一个对于“对象的描述”，对应于内置函数 str() 经常用于 print()方法，帮助我们查看对象的信息。`__str__()`可以重写。
    """
    def __str__(self):
        return f"名字是：{self.name},年龄是：{self.__age}"


    def say_company(self):
        print("我的公司是：", Employee.__company) # 类内部可以直接访问私有属性
        print(self.name, "的年龄是：", self.__age)
        self.__work()

    # 定义私有实例方法 通过 dir 可以查到_Employee__work
    def __work(self):
        print("好好工作，月月加薪！")

    @property
    def salary(self):
        return salary

    # 相当于 salary 属性的 setter 方法
    @property.setter
    def salary(self, salary):
        self.salary = salary



print("Employee 类 test---->")
emploee = Employee("liuzhen", 25)
print(emploee.name)  # liuzhen
print(dir(emploee))  # ['_Employee__age', '_Employee__company', '_Employee__work', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'name', 'say_company']
emploee.say_company()  # liuzhen 的年龄是： 25 好好工作，月月加薪！
# 通过这种方式访问私有属性
print(emploee._Employee__age)  # 25

salary = emploee.salary
print("工资是：", salary)
# emploee.salary() # 报错，它是属性，不能这样调用

# 报错：AttributeError: can't set attribute  因为@property修饰的属性，如果没有加setter方法，则只为只读属性！
# emploee.salary = 1000

