# coding=utf-8
# 多种事件绑定方式汇总
from tkinter import *

root = Tk();root.geometry("270x30")


def mouseTest1(event):
    print("bind()方式绑定，可以获取event对象")
    print(event.widget)


def mouseTest2(a, b):
    print("a={0},b={1}".format(a, b))
    print("command方式绑定，不能直接获取event对象")


def mouseTest3(event):
    print("右键单击事件，绑定给所有按钮啦！！")
    print(event.widget)


b1 = Button(root, text="测试bind()绑定")
b1.pack(side="left")
# bind方式绑定事件
b1.bind("<Button-1>", mouseTest1)

# command属性直接绑定事件
b2 = Button(root, text="测试command2",
       command=lambda: mouseTest2("gaoqi", "xixi"))
b2.pack(side="left")


# 给所有Button按钮都绑定右键单击事件<Button-2>
b1.bind_class("Button", "<Button-2>", mouseTest3)

root.mainloop()