#!/usr/bin/env python
# encoding: utf-8
import copy

'''
SyntaxError: Non-ASCII character '\xe6' in file D:/Code/PythonWorkSpace/PythonScript/study_test/demo01.py on line 32, but no encoding declared;
在第一行加上：# encoding: utf-8
'''

a = 50
b = 40

if a >= 45:
    c = a
    print(c)
elif a > 100:
    print(100)
else:
    print(200)

a = 1
while True:
    print(a)
    a = a + 1
    if a == 5:
        break
print("--------->")

for i in range(100):
    print(i)
print("--------->")

a = [100, 54, 33, 2, 55]
a.sort()
for i in a:
    print(i)
    if i == 54:
        break
else:
    print("我在for循环里执行了else语句")

print("--------------------->")

'''
这个add函数有注释
'''


def add(a, b):
    return a + b


print(add(100, 200))

C = '400'


def changeC():
    # 改变全局变量的值必须在方法内加 global 关键字修饰，不然全局变量的值不能改变
    global C
    C = '122'
    print("C的值为：" + C)


print("aaaaaaaaaaaaaa==>")
changeC()

d = copy.copy(C)


class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def printUser(self):
        print("name: " + self.name)
        print("age: " + str(self.age))

    def printUser(self, sex):
        print('sex->')


user = User("刘振", 23)
user.printUser('1')
