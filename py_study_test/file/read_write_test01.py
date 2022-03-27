# coding:utf-8

"""
infile = open(name,'rw')
python 中文件打开操作的mode中没有“rw”
合法的mode有：
r、rb、r+、rb+、w、wb、w+、wb+、a、ab、a+、ab+
"""

# with open(r"f1.txt","w") as f1:
#     s = ["高淇\n","高老三\n","高老四\n"]
#     f1.writelines(s)
#     s2 = "开始写\n换行1\naaaa"
#     f1.write(s2)
#     print "写成功"

try:
    f2 = open(r"file2.txt", "w")
    s = "开始写\n换行1\n换行2"
    print(s)
    f2.write(s)
except BaseException as e:
    print(e)

finally:
    f2.close()




