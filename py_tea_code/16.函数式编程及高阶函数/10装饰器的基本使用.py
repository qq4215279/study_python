#使用装饰器 完成不修改fun1() fun2()函数的源码，添加输出日志信息
import time


def writeLog(func):
    try:
        file=open('log.txt','a',encoding='utf-8')
        file.write('访问：')
        file.write(func.__name__)
        file.write('\t')
        file.write('时间：')
        file.write(time.asctime())
        file.write('\n')
    except Exception as e:
        print(e.args)
    finally:
        file.close()

#使用闭包
def funcOut(func):
    def funcIn():
        writeLog(func)
        func()
    return funcIn
#闭包的调用

@funcOut  #fun1=funcOut(fun1)
def fun1():
    print('功能1')

@funcOut
def fun2():
    print('功能2')
fun1()
fun2()