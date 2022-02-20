#coding=utf-8
print("step0")
try:
    print("step1")
    a = 3/2
    print("step2")
except BaseException as e:
    print("step3")
    print(e)
    print(type(e))
print("end!!!!")