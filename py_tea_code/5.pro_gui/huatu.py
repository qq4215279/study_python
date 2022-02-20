#coding=utf-8
from tkinter import *
from tkinter.colorchooser import *



x,y=0,0    #鼠标坐标
startDrawFlag = False   #是否开始画画
lastDraw = 0   #最后绘制图形的id

bgcolor="#000000";fgcolor="#ff0000"
win_width=900;win_height=450

root = Tk();root.geometry(str(win_width)+"x"+str(win_height)+"+400+400")
root.title("画图软件核心实现")

c1 = Canvas(root,width=win_width,height=win_height*0.8,bg=bgcolor)
c1.pack()

def myDrawPen(event):
    global x,y,startDrawFlag

    #print("鼠标位置(相对于父容器)：({0},{1})".format(event.x, event.y))
    if startDrawFlag==False:
        startDrawFlag=True
        x = event.x; y=event.y

    c1.create_line(x,y,event.x,event.y,fill=fgcolor)
    x = event.x;
    y = event.y;

def stopDraw(event):
    global startDrawFlag,lastDraw
    startDrawFlag = False
    print("不能画")

    lastDraw = 0


def myDrawRect(event):
    global x,y,startDrawFlag,lastDraw

    c1.delete(lastDraw)

    if startDrawFlag==False:
        startDrawFlag=True
        x = event.x; y=event.y

    lastDraw = c1.create_rectangle(x,y,event.x,event.y,outline=fgcolor)

def myEraser(event):
    global x, y, startDrawFlag, lastDraw

    if startDrawFlag == False:
        startDrawFlag = True

    c1.create_rectangle(event.x - 4, event.y - 4, event.x + 4, event.y + 4,outline=bgcolor,fill=bgcolor)

def myLine(event):
    global x,y,startDrawFlag,lastDraw

    c1.delete(lastDraw)

    if startDrawFlag==False:
        startDrawFlag=True
        x = event.x; y=event.y

    lastDraw = c1.create_line(x, y, event.x, event.y, fill=fgcolor)

def myLineArrow(event):
    global x,y,startDrawFlag,lastDraw

    c1.delete(lastDraw)

    if startDrawFlag==False:
        startDrawFlag=True
        x = event.x; y=event.y

    lastDraw = c1.create_line(x, y, event.x, event.y, fill=fgcolor,arrow=LAST)


#进入程序以及点击操作按钮后的事件管理
def myEventManager(event):

    name = event.widget.winfo_name()
    c1.bind("<ButtonRelease-1>", stopDraw)

    if name == "rect":
        c1.bind("<B1-Motion>", myDrawRect)
    elif name == "clear":
        c1.delete("all")
    elif name == "eraser":
        c1.bind("<B1-Motion>",myEraser)
    elif name == "line":
        c1.bind("<B1-Motion>",myLine)
    elif name == "lineArrow":
        c1.bind("<B1-Motion>",myLineArrow)
    elif name == "chooseColor":
        global fgcolor
        c = askcolor(color=fgcolor,title="选择画笔颜色")
        print(c)  #((225.87890625, 3.01171875, 30.1171875), '#e1031e')
        fgcolor = c[1]
    else: #画笔
        c1.bind("<B1-Motion>", myDrawPen)

f1 = Frame(root);f1.pack()
btn_start = Button(f1,text="开始",name="start");btn_start.pack(side="left",padx="10")
btn_pen = Button(f1,text="画笔",name="pen");btn_pen.pack(side="left",padx="10")
btn_rect = Button(f1,text="画矩形",name="rect");btn_rect.pack(side="left",padx="10")
btn_clear = Button(f1,text="清屏",name="clear");btn_clear.pack(side="left",padx="10")
btn_eraser = Button(f1,text="橡皮擦",name="eraser");btn_eraser.pack(side="left",padx="10")
btn_line = Button(f1,text="直线",name="line");btn_line.pack(side="left",padx="10")
btn_lineArrow = Button(f1,text="直线(箭头)",name="lineArrow");btn_lineArrow.pack(side="left",padx="10")
btn_color = Button(f1,text="颜色",name="chooseColor");btn_color.pack(side="left",padx="10")
#给所有按钮处理事件
btn_pen.bind_class("Button","<1>",myEventManager)

#处理快捷键
def kuaijiejian(event):
    global fgcolor
    if event.char == "r":
        fgcolor = "#ff0000"
    elif event.char =="g":
        fgcolor = "#00ff00"
    elif event.char == "y":
        fgcolor = "#ffff00"

root.bind("<KeyPress-r>",kuaijiejian)
root.bind("<KeyPress-g>",kuaijiejian)
root.bind("<KeyPress-y>",kuaijiejian)


root.mainloop()
