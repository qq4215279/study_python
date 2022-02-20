# coding=utf-8

# 测试try...except...else结构
try:
    a = input("请输入一个被除数：")
    b = input("请输入一个除数：")
    c = float(a) / float(b)
except BaseException as e:
    print(e)
else:
    print(c)
print("程序结束！")
