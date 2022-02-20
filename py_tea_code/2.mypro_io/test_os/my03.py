#coding=utf-8
#测试os.path中关于目录、路径的操作

import os
import os.path      #from os import path

############判断：绝对路径、是否目录、是否文件、文件是否存在#############
print(os.path.isabs("d:/a.txt"))    #True
print(os.path.isdir("d:/a.txt"))   #False
print(os.path.isfile("d:/a.txt"))  #True
print(os.path.exists("d:/a.txt"))

##############获得文件基本信息################
print(os.path.getsize("b.txt"))
print(os.path.abspath("b.txt"))
print(os.path.dirname("d:/a.txt"))

print(os.path.getctime("b.txt"))
print(os.path.getatime("b.txt"))
print(os.path.getmtime("b.txt"))

##############对路径的操作#####################
path = os.path.abspath("b.txt")
print(os.path.split(path))
print(os.path.splitext(path))

print(os.path.join("aa","bb","cc"))