#coding=utf-8
#测试调试、断点

def aa():
    print("run in aa() start!")
    print("step1")
    num1 = 3
    num2 = num1*4
    print("step2")
    print("run in aa()  end!")

if __name__=="__main__":
    print("step1")
    aa()
    print("step2")
