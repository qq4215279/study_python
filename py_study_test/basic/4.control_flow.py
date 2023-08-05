# encoding: utf-8

'''
控制语句
'''

'''
一：选择结构：
1. 单分支选择结构
    if 条件表达式:
	    语句/语句块
2. 双分支选择结构
    if 条件表达式 :
	    语句 1/语句块 1
    else:
	    语句 2/语句块 2
3. 多分支结构
    if 条件表达式 1 :
	    语句 1/语句块 1
    elif 条件表达式 2:
	    语句 2/语句块 2
	...
    elif 条件表达式 n :
	    语句 n/语句块 n
    [else:
	    语句 n+1/语句块 n+1
    ]
4. 选择结构可以嵌套
    if 表达式 1：
	    语句块 1
	    if 表达式 2：
		    语句块 2
	    else:
		    语句块 3
    else:
	    if 表达式 4：
		    语句块 4
		    
三元条件运算符: 条件为真时的值 if(条件表达式) else 条件为假时的值
'''
# 1.
# num = input("请输入数字：")
num = 100
if int(num) >= 100:
    print(num)

a = 50
b = 40
if a >= 45:
    c = a
    print(c)
elif a > 100:
    print(100)
else:
    print(200)

# 三目表达式
num = 11
res = num if num >= 100 else "数字太小了，不打印！"
print(res)

#
# score = int(input("请输入一个在0-100之间的数字："))
score = 90
grade = ""
if score > 100 or score < 0:
    score = int(input("输入错误！请重新输入一个在0-100之间的数字："))
else:
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    elif score >= 60:
        grade = 'D'
    else:
        grade = 'E'
    print("分数为{0},等级为{1}".format(score, grade))

# 或者也可以用下面代码更少的方法。不过，需要大家思考为什么这么写了
# score = int(input("请输入一个在0-100之间的数字："))
score = 99
degree = "ABCDE"
num = 0
if score > 100 or score < 0:
    score = int(input("输入错误！请重新输入一个在0-100之间的数字："))
else:
    num = score // 10
if num < 6:
    num = 5
    print("分数是{0},等级是{1}".format(score, degree[9 - num]))

'''
二、循环结构
1. while 循环
    while 条件表达式:
	    循环体语句
	else:
	    语句块
2. for 循环
    for 变量 in 可迭代对象:
	    循环体语句
	else:
	    语句块
注：可迭代对象：
    1. 序列。包含：字符串、列表、元组
    2. 字典
    3. 迭代器对象（iterator）
    4. 生成器函数（generator）
    5. 文件对象
    
range 对象: 格式为: range(start, end [,step])	    
'''
num = 10
while num < 12:
    print("while循环：num = " + str(num))
    num = num + 1
else:
    print("111")

# 可迭代对象 -- for循环
for x in [10, 20, 30]:
    print("for循环：x = " + str(x))

for x in range(10):
    if x < 5:
        print("range for 循环 x * 2 = " + str(x * 2))
    elif x == 7:
        print("x==7 跳过...")
        continue
    elif x == 8:
        print("x == 8时，直接结束循环")
        break

'''
字典推导式:
格式如下：{key_expression : value_expression for 表达式 in 可迭代对象}
类似于列表推导式，字典推导也可以增加 if 条件判断、多个 for 循环。
'''
my_text = ' i love you, i love sxt, i love gaoqi'
char_count = {c: my_text.count(c) for c in my_text}
print("字典推导式:")
print(char_count)

'''
集合推导式:
集合推导式生成集合，和列表推导式的语法格式类似：`{表达式 for item in 可迭代对象 }`
或者：{表达式 for item in 可迭代对象 if 条件判断}
'''
res = {x for x in range(1, 100) if x % 9 == 0}
print("集合推导式: ")
print(res)

'''
生成器推导式（生成元组）
“一个生成器对象”。显然，元组是没有推导式的。
一个生成器只能运行一次。第一次迭代可以得到数据，第二次迭代发现数据已经没有了。
'''
print("生成元组test：")
gnt = (x for x in range(1, 100) if x % 9 == 0)
for x in gnt:
    print(x, end=' ')
for x in gnt:
    print(x, end=' ')
