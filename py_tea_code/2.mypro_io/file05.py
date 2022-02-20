#测试文件读取
with open(r"e.txt","r",encoding="utf-8") as f:
    str = f.read(3)
    print(str)