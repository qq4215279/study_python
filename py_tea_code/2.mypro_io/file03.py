#使用异常机制管理文件对象的关闭操作
try:
    f = open(r"c.txt","w")
    strs = ["aa\n","bb\n","cc\n"]
    f.writelines(strs)
except BaseException as e:
    print(e)
finally:
    f.close()