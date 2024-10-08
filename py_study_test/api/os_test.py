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
zhou_path = "file/电影/港台/周星驰"
b_path = "file/电影/港台/周星驰/bb"
# 3. os.mkdir(path)  创建目录。注：1. 创建已存在的目录会抛异常！2. 若父级目录不存在，无法创建子目录/文件
# os.mkdir(f"{zhou_path}/bb")

# 4. os.remove(path)  删除指定的文件。注：若文件不存在，抛异常！解决: shutil.rmtree(dir)  递归删除dir下的所有文件和目录
# os.remove(f"{zhou_path}/bb")

# 5. os.makedirs(path1/path2/path3/... )  创建多级目录。可递归创建不存在的父目录
# os.makedirs(zhou_path)
# os.makedirs("./file/音乐/香港/刘德华") # ./ 指当前目录   ../指的是上一级目录

# 6. os.rmdir(path)  删除目录。注：1. path不存在会抛异常！2. 若当前目录还有子目录或文件，则抛异常！3. 只能删除单个子目录，不能删除文件
# os.rmdir(zhou_path)  # 相对路径都是相对于当前的工作目录

# 7. os.removedirs(path1/path2...)  删除多级目录。注： 若当前path下还有子目录或文件，则抛异常！只能删除空目录！
# os.removedirs(b_path)  #
# os.removedirs("./file/音乐/香港/刘德华")  # 只能删除空目录

# 8. os.rename(src, dest)  重命名文件或目录
# os.rename("file/电影", "电影")

# 9. os.listdir(path) 返回 path 目录下的文件和目录列表
# listdir_test()

# 10. os.getcwd() 返回当前工作目录：current work dir
# print("返回当前工作目录：" + os.getcwd())


# 11. os.chdir(path)  把 path 设为当前工作目录
# os.chdir("d:") # 改变当前的工作目录为：d:盘根目录

# 12. os.walk()  递归遍历所有文件和目录
"""
os.walk()方法：返回一个 3 个元素的元组，(dirpath, dirnames, filenames), 
    dirpath：要列出指定目录的路径
    dirnames：目录下的所有文件夹
    filenames：目录下的所有文件    
"""
# walk_demo()

# 13. sep 当前操作系统所使用的路径分隔符
# print(os.sep)  # windows -> \    linux 和 unix -> /

# 14. stat(path) 返回文件的所有属性
# print(os.stat("os_test.py"))

# 15. name
# print(os.name)  # windows -> nt   linux 和 unix -> posix

# 16. linesep
print(repr(os.linesep))  # windows -> \r\n   linux -> \n

# 17. getlogin()  获取系统登录用户（获取在进程的控制终端上登录的用户的名称。）
print(os.getlogin())


# eg:
# 9. 列出指定目录下所有的.py 文件，并输出文件名
def listdir_test():
    # 返回当前工作目录
    work_dir = os.getcwd()
    file_list = os.listdir(work_dir)  # 列出子目录和子文件
    for filename in file_list:
        pos = filename.rfind(".")
        if filename[pos + 1:] == "py":
            print(filename, end="\t")
    print("##################")
    file_list2 = [filename for filename in os.listdir(work_dir) if
                  filename.endswith(".py")]
    for filename in file_list2:
        print(filename, end="\t")

# 12.
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

listdir_test()