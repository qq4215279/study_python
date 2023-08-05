# coding:utf-8

"""
infile = open(name,'rw')
python 中文件打开操作的mode中没有“rw”
合法的mode有：
    r 只读、rb 二进制只读、r+ 读写、rb+ 二进度读写、
    w 写、wb 二进制读写、w+ 读写、wb+ 二进制读写读写、
    a 追加、ab 二进制追加、a+ 读写追加、ab+ 二进制读写追加
规则：(r w a) 与 (b +) 进行排列组合
含义：
    'r'：只读模式
    'w'：只写模式（会截断文件）
    'a'：追加模式
    'x'：创建并写入模式
    'b'：二进制模式
    't'：文本模式
    '+'：读写模式（与其他模式一起使用）

文本文件的写入
    write(a) 把字符串 a 写入到文件中
    writelines(b) 把字符串列表写入文件中，不添加换行符
    close() 关闭文件流。由于文件底层是由操作系统控制，所以我们打开的文件对象必须显式调用 close()方法关闭文件对象。
        当调用 close()方法时，首先会把缓冲区数据写入文件(也可以直接调用 flush()方法)，再关闭文件，释放文件对象。
    flush()


文本文件的读取
    文件的读取一般使用如下三个方法：
    read([size]) 从文件中读取 size 个字符，并作为结果返回。如果没有 size 参数，则读取整个文件。读取到文件末尾，会返回空字符串。
    readline() 读取一行内容作为结果返回。读取到文件末尾，会返回空字符串。
    readlines() 文本文件中，每一行作为一个字符串存入列表中，返回该列表
    tell() ？？？

with 是 Python 中的一个关键字，用于创建一个上下文管理器（Context Manager）。上下文管理器用于管理代码块的进入和退出，它可以确保资源在使用完毕后被正确地释放，无论代码块中是否发生了异常。
    使用 with 关键字可以更简洁、更安全地管理资源，比如文件操作、网络连接、数据库连接等。
   语法：
        with context_expression [as target]:
            with-block

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


"""
with 使用
"""
# 1. 文件操作：文件会在代码块结束后自动关闭
with open('file.txt', 'r') as file:
    content = file.read()

# 2. 数据库连接：数据库连接会在代码块结束后自动关闭
# with connect_database() as db:
#     data = db.query('SELECT * FROM table')


# 3. 网络连接：网络连接会在代码块结束后自动关闭！
# with open_socket() as socket:
#     data = socket.receive()
