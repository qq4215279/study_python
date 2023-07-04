# encoding: utf-8

'''
单例模式
单例模式（Singleton Pattern）的核心作用是确保一个类只有一个实例，并且提供一个访问该实例的全局访问点。
单例模式只生成一个实例对象，减少了对系统资源的开销。当一个对象的产生需要比较多的资源，如读取配置文件、产生其他依赖对象时，可以产生一个“单例对象”，
然后永久驻留内存中，从而极大的降低开销。
单例模式有多种实现的方式，我们这里推荐重写__new__()的方法。
'''
class MySingleton:
    __obj = None
    __init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)

        return cls.__obj

    def __init__(self, name):
        if MySingleton.__init_flag:
            print("init...")
            self.name = name
            MySingleton.__init_flag == False

instance1 = MySingleton("liuzhen")
print(instance1)
print(instance1.name)

instance2 = MySingleton("hahaha")
print(instance2)
print(instance1.name)

print("---------------->")

class CarFactory:
    __obj = None
    __init_flag = True

    def create_car(self, brand):
        if brand == "奔驰":
            return Benz()
        elif brand == "宝马":
            return BMW()
        elif brand == "比亚迪":
            return BYD()
        else:
            return "未知品牌，无法创建"


    def __new__(cls, *args, **kwargs):
        if cls.__obj == None:
            cls.__obj = object.__new__(cls)
        return cls.__obj

    def __init__(self):
        if CarFactory.__init_flag:
            print("init CarFactory ...")
            CarFactory.__init_flag = False



class Benz:
    pass

class BMW:
    pass

class BYD:
    pass

factory = CarFactory()
c1 = factory.create_car("奔驰")
c2 = factory.create_car("宝马")
print(c1)
print(c2)

factory2 = CarFactory()
print(factory)
print(factory2)
