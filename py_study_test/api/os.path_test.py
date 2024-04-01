# coding = utf-8

import os.path
import sys

"""
os.path 模块提供了目录相关（路径判断、路径切分、路径连接、文件夹遍历）的操作
"""

a_path = "api2/电影/港台/周星驰/a"
a_dir = "api2/电影/港台/周星驰"

# 测试 os.path 常用方法
# 1. os.path.isdir(path)  判断 path 是否为目录
# print(os.path.isdir("api2/电影/港台/周星驰"))  # True
# print(os.path.isdir(a_path))  # False

# 2. os.path.isfile(path)  判断 path 是否为文件
# print(os.path.isfile(a_path))  # True

# 3. os.path.exists(path)  判断指定路径的文件或目录是否存在
# print(os.path.exists(a_path))  # 文件是否存在

# 4. os.path.getsize(filename)  返回文件的大小
# print(os.path.getsize(a_path))  # 0

# 5. os.path.isabs(path)  判断 path 是否绝对路径
# print(os.path.isabs(a_path))  # False

# 6. os.path.abspath(path)  返回绝对路径
# print(os.path.abspath(a_path))  # 输出绝对路径  D:\Code\PythonWorkSpace\study_python\py_study_test\api\api2\a.txt

# 7. os.path.dirname(path)  获取目录路径部分
# print(os.path.dirname(a_path))  # api2/电影/港台/周星驰

# 8. os.path.getatime(filename)  返回文件的最后访问时间
# print(os.path.getctime(a_path))  # 1711960587.35217

# 9. os.path.getmtime(filename)  返回文件的最后修改时间
# print(os.path.getatime(a_path))  # 1711960587.35217

# 10. os.path.walk(top,func,arg)  递归方式遍历目录

# 11. os.path.join(path, *paths)  连接多个 path
# print(os.path.join("aa", "bb", "cc"))  # 返回路径：aa\bb\cc

# 12.1. os.path.split(path)  对路径进行分割，以列表形式返回
a_abspath = os.path.abspath(a_path)  # 返回绝对路径
# print(os.path.split(a_abspath))  # 返回元组：目录、文件 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api', 'a.txt')

# 12.2. __file__ 获取文件所在绝对路径
# print("curPath: ", __file__)

# 13. os.path.splitext(path)  从路径中分割文件的扩展名
# print(os.path.splitext(path3))  # 返回元组：路径、扩展名 ('D:\\Code\\PythonWorkSpace\\study_python\\py_study_test\\api\\api2\\a', '.txt')

# 14. os.path.expanduser("~")  获取用户目录
# print(os.path.expanduser("~"))  # C:\Users\D0381

