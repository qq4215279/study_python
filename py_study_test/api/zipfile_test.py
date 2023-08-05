# coding = utf-8

import shutil
import zipfile

# 【示例1】实现将文件夹所有内容压缩(使用 shutil 模块)
# 将"电影/港台"文件夹下所有内容压缩到"音乐2"文件夹下生成电影.zip
shutil.make_archive("音乐/电影", "zip", "file/电影/港台")

# 压缩:将指定的多个文件压缩到一个 zip 文件
z = zipfile.ZipFile("file/a.zip", "w")
z.write("a.txt")
z.write("2.txt")
z.close()

# 【示例2】实现将压缩包解压缩到指定文件夹(使用 shutil 模块)
# 解压缩：
z2 = zipfile.ZipFile("file/a.zip", "r")
z2.extractall("d:/")  # 设置解压的地址
z2.close()
