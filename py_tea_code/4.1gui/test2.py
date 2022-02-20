import hello

a = hello.add(30,40)
# add(100,200)      #不加模块名无法识别
print(a)


from hello import *

a = add(100,200)    #无需模块名，可以直接引用里面的函数/类
print(a)

b = MyNum()
b.print123()