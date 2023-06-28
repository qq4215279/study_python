# coding=utf-8
import os

"""
os 模块 - 调用操作系统命令
可以帮助我们直接对操作系统进行操作。我们可以直接调用操作系统的可执行文件、命令，直接操作文件、目录等等。在系统运维的核心基础。
"""

# 1. os.system() 可以帮助我们直接调用系统的命令
# os.system("notepad.exe")  # 调用 windows 系统的记事本程序
# os.system("ping www.baidu.com")  # 调用 windows 系统中 ping 命令

# 2. os.startfile() 直接调用可执行文件
# os.startfile(r"D:\Install\App\微信\WeChat\WeChat.exe")  # 运行安装好的微信

# 常用操作文件的方法
# 目录操作的相关方法
# 3. mkdir(path)  创建目录
# os.mkdir("书籍")

# 4. makedirs(path1/path2/path3/... )  创建多级目录
# os.makedirs("电影/港台/周星驰")
# os.makedirs("./音乐/香港/刘德华") # ../指的是上一级目录

# 5. rmdir(path)  删除目录
# os.rmdir("书籍")  # 相对路径都是相对于当前的工作目录

# 6. removedirs(path1/path2...)  删除多级目录
# os.removedirs("电影/港台/周星驰")  # 只能删除空目录
# os.removedirs("./音乐/香港/刘德华")  # 只能删除空目录

# 7. remove(path)  删除指定的文件
# os.remove("D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\file\\testXLS.xls")

# 8. rename(src, dest)  重命名文件或目录
# os.rename("电影", "电影")

# 9. listdir(path) 返回 path 目录下的文件和目录列表
# dirs = os.listdir("电影")
# print(dirs)

# 10. getcwd() 返回当前工作目录：current work dir
# print("返回当前工作目录：" + os.getcwd())


# 11. chdir(path)  把 path 设为当前工作目录
# os.chdir("d:") # 改变当前的工作目录为：d:盘根目录

# 12. walk()  递归遍历所有文件和目录
"""
os.walk()方法：返回一个 3 个元素的元组，(dirpath, dirnames, filenames), 
    dirpath：要列出指定目录的路径
    dirnames：目录下的所有文件夹
    filenames：目录下的所有文件
"""


def walk_demo():
    all_dirs = []
    all_files = []
    path = os.getcwd()
    list_files = os.walk(path)
    for dirpath, dirnames, filenames in list_files:
        print("print dirPath ---------->")
        print(dirpath)
        print("print dirNames ---------->")
        for dirName in dirnames:
            print(dirName)
            all_dirs.append(os.path.join(dirpath, dirName))

        print("print fileNames ---------->")
        for fileName in filenames:
            print(fileName)
            all_files.append(os.path.join(dirpath, fileName))

    print("all dirs: ==================================>")
    for dirName in all_dirs:
        print(dirName)

    print("all files: ")
    # 打印子目录和子文件
    for file in all_files:
        print(file)


# walk_demo()

# 13. sep 当前操作系统所使用的路径分隔符
# print(os.sep)  # windows -> \    linux 和 unix -> /

# 14. stat(path) 返回文件的所有属性
# print(os.stat("os_test.py"))

# 15. name
# print(os.name)  # windows -> nt   linux 和 unix -> posix

# 16. linesep
print(repr(os.linesep))  # windows -> \r\n   linux -> \n
