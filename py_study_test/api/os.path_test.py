# coding = utf-8

import os.path

"""
os.path 模块提供了目录相关（路径判断、路径切分、路径连接、文件夹遍历）的操作
"""

# 测试 os.path 常用方法
# 1. isabs(path)  判断 path 是否绝对路径
# print(os.path.isabs("d:/a.txt"))  # 是否绝对路径

# 2. isdir(path)  判断 path 是否为目录
# print(os.path.isdir("d:/a.txt"))  # 是否目录

# 3. isfile(path)  判断 path 是否为文件
# print(os.path.isfile("d:/a.txt"))  # 是否文件

# 4. exists(path)  判断指定路径的文件是否存在
# print(os.path.exists("d:/a.txt"))  # 文件是否存在

# 5. getsize(filename)  返回文件的大小
# print(os.path.getsize("a.txt"))  # 文件大小

# 6. abspath(path)  返回绝对路径
# print(os.path.abspath("a.txt"))  # 输出绝对路径  D:\Code\PythonWorkSpace\study_python\py_study_test\api\a.txt

# 7. dirname(p)  返回目录的路径
# print(os.path.dirname("d:/a.txt"))  # 输出所在目录

# 8. getatime(filename)  返回文件的最后访问时间
# print(os.path.getctime("a.txt"))  # 返回创建时间

# 9. getmtime(filename)  返回文件的最后修改时间
# print(os.path.getatime("a.txt"))  # 返回最后访问时间
# print(os.path.getmtime("a.txt"))  # 返回最后修改时间

# 10. walk(top,func,arg)  递归方式遍历目录

# 11. join(path, *paths)  连接多个 path
# print(os.path.join("aa", "bb", "cc"))  # 返回路径：aa\bb\cc

# 12. split(path)  对路径进行分割，以列表形式返回
path = os.path.abspath("D:/Code/PythonWorkSpace/study_python/py_study_test/api/a.txt")  # 返回绝对路径
# print(os.path.split(path))  # 返回元组：目录、文件 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api', 'a.txt')
path2 = os.path.abspath("D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api\\a.txt")  # 返回绝对路径
# print(os.path.split(path2))  # 返回元组：目录、文件 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api', 'a.txt')

path3 = os.path.abspath("a.txt")  # 返回绝对路径
# print(os.path.split(path3))  # 返回元组：目录、文件 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api', 'a.txt')

# 13. splitext(path)  从路径中分割文件的扩展名
# print(os.path.splitext(path3))  # 返回元组：路径、扩展名 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api\\a', '.txt')


# 列出指定目录下所有的.py 文件，并输出文件名
def listdir_test():
    path = os.getcwd()
    file_list = os.listdir(path)  # 列出子目录和子文件
    for filename in file_list:
        pos = filename.rfind(".")
        if filename[pos + 1:] == "py":
            print(filename, end="\t")
    print("##################")
    file_list2 = [filename for filename in os.listdir(path) if
                  filename.endswith(".py")]
    for filename in file_list2:
        print(filename, end="\t")

listdir_test()