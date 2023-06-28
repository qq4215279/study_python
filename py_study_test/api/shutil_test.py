# coding = utf-8

import shutil

"""
shutil 模块是 python 标准库中提供的，主要用来做文件和文件夹的拷贝、移动、删除等；还可以做文件和文件夹的压缩、解压缩操作。
os 模块提供了对目录或文件的一般操作。shutil 模块作为补充，提供了移动、复制、压缩、解压等操作，这些 os 模块都没有提供
"""

# copy 文件内容
shutil.copyfile("a.txt", "a_copy.txt")

# 实例：实现递归的拷贝文件夹内容
# "音乐"文件夹不存在才能用。
# shutil.copytree("电影/学习", "音乐", ignore=shutil.ignore_patterns("*.html", "*.htm"))
