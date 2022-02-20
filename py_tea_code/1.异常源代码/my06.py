# coding=utf-8

# 测试try...except...else...finally结构
try:
    a = input("请输入一个被除数：")
    b = input("请输入一个除数：")
    c = float(a) / float(b)
except BaseException as e:
    print(e)
else:
    print(c)
finally:
    print("我是finally中的语句，无论发生异常与否，都执行！")
print("程序结束！")
