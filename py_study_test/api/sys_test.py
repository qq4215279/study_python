# encoding:utf-8

import sys

"""
sys 是 Python 标准库中的一个模块，提供了访问 Python 解释器的一些变量和函数。以下是 sys 模块的一些常用功能：

1. sys.argv: 命令行参数，在解释器启动后, argv 列表包含了传递给脚本的所有参数, 列表的第一个元素为脚本自身的名称。
        sys.argv[0]:表示程序自身
        sys.argv[1]: 表示程序的第一个参数
        sys.argv[2]: 表示程序的第二个参数

2. sys.exit([arg]): 退出程序，可选的参数 arg 是退出时的返回码。正常退出时exit(0)。

3. 输入: sys.stdin.readline() 与 input()
    sys.stdin.readline(): 方式与input方式的区别是: len(aa)元素中多了一个‘\n’换行符。即sys.stdin.readline() 方式会读入换行符。
    input(): 里面可以直接传入文本，然后打印出来。

4. 输出: sys.stdout.write() 与 print()
    注意：sys.stdout.write(obj+‘\n’)中的obj只能是字符串。
    4.2. sys.stdout.reconfigure(encoding='utf-8')  设置默认编码为 UTF-8

5. sys.stderr: 错误流，标准错误流的文件对象。

6. Python 解释器的信息:
    6.1. sys.version: 获取Python解释程序的版本信息。
    6.2. sys.platform: 返回平台标识符，例如 'win32' 或 'linux'。

7. sys.path
    当我们导入一个模块时: import xxx ，默认情况下python解释器会搜索当前目录、已安装的内置模块和第三方模块。
    搜索路径存放在sys模块的path中。【即默认搜索路径可以通过sys.path打印查看】

8. sys.path.append()
    对于需要引用的模块和需要执行的脚本文件不在同一个目录时，可以按照如下形式来添加路径
    eg: 需要引用 F:\Code\PythonSpace\study_python\py_study_test\daily\command.py
        sys.path.append('F:\Code\PythonSpace\study_python\py_study_test\daily')

9. 其他    
    # sys.modules.keys() 返回所有已经导入的模块列表
    # sys.exc_info() 获取当前正在处理的异常类,exc_type、exc_value、exc_traceback当前处理的异常详细信息
    # sys.hexversion 获取Python解释程序的版本值，16进制格式如：0x020403F0
    # sys.maxint 最大的Int值
    # sys.maxunicode 最大的Unicode值
    # sys.modules 返回系统导入的模块字段，key是模块名，value是模块
    # sys.exc_clear()   用来清除当前线程所出现的当前的或最近的错误信息
    # sys.exec_prefix   返回平台独立的python文件安装的位置
    # sys.byteorder         本地字节规则的指示器，big-endian平台的值是'big',little-endian平台的值是'little'
    # sys.copyright         记录python版权相关的东西
    # sys.api_version   解释器的C的API版本
    # sys.getwindowsversion  获取Windows的版本
    # sys.getdefaultencoding  返回当前你所用的默认的字符编码格式
    # sys.getfilesystemencoding 返回将Unicode文件名转换成系统文件名的编码的名字
    # sys.setdefaultencoding(name) 用来设置当前默认的字符编码
    # sys.builtin_module_names  Python解释器导入的模块列表
    # sys.executable                   Python解释程序路径


"""

# 1. 打印命令行参数
print("1. 命令行参数:", sys.argv)

# 2. 退出程序
# sys.exit(999)  # 也可以使用 sys.exit(999) 指定退出码

print("6.1. 查看python解释器版本: ", sys.version)
print("6.2. 操作系统平台名称", sys.platform)

print("7. 打印默认搜索路径", sys.path)
sys.path.append('F:/Code/PythonSpace/study_python/py_study_test/daily')

print("7. 打印默认搜索路径", sys.path)

# 3. 输入
def input_read_demo():
    print('请输入内容(ys.stdin.readline())：', end='')
    aa = sys.stdin.readline()  # sys.stdin.readline() 相当于input，区别在于input不会读入'\n'
    bb = input('请输入内容(input)：')

    print(len(aa))
    print(len(bb))

# 4. 输出
def output_write_demo():
    print('请输入内容(sys.stdin.readline)：', end='')
    aa = sys.stdin.readline()  # sys.stdin.readline() 相当于input，区别在于input不会读入'\n'
    bb = input('请输入内容(input)：')

    sys.stdout.write(str(len(aa)))
    print(len(bb))

    sys.stdout.write(str(len(aa)) + '\n')  # 默认无法实现print方式的sep参数功能，所以需要手动在后面添加一个换行符
    print(len(bb))

if __name__ == '__main__':
    input_read_demo()
    output_write_demo()
