# coding=utf-8


# 测试finally
try:
    f = open("d:/adddd.txt", "r")
    content = f.readline()
    print(content)
except:
    print("文件未找到")
finally:
    print("run in finally。关闭资源")
    try:
        f.close()
    except BaseException as e:
        print(e)

print("程序执行结束！")
