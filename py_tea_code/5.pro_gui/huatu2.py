"""开发画图软件的菜单
"""

from tkinter.filedialog import *
from tkinter.colorchooser import *

#窗口的宽度和高度
win_width=900
win_height=450

class Application(Frame):

    def __init__(self, master=None,bgcolor="#000000"):
        super().__init__(master)        # super()代表的是父类的定义，而不是父类对象
        self.master = master
        self.bgcolor = bgcolor
        self.fgcolor = "#ff0000"
        self.x = 0
        self.y = 0  # 鼠标坐标
        self.startDrawFlag = False  # 是否开始画画
        self.lastDraw = 0  # 最后绘制图形的id

        self.drawpad = None         #绘图区canvas对象

        self.pack()
        self.createWidget()

    def createWidget(self):
        #绘图区
        self.drawpad = Canvas(root, width=win_width, height=win_height*0.8, bg=self.bgcolor)
        self.drawpad.pack()

        # 创建操作按钮
        btn_start = Button(root, text="开始", name="start")
        btn_start.pack(side="left", padx="10")
        btn_pen = Button(root, text="画笔", name="pen")
        btn_pen.pack(side="left", padx="10")
        btn_rect = Button(root, text="画矩形", name="rect")
        btn_rect.pack(side="left", padx="10")
        btn_clear = Button(root, text="清屏", name="clear")
        btn_clear.pack(side="left", padx="10")
        btn_eraser = Button(root, text="橡皮擦", name="eraser")
        btn_eraser.pack(side="left", padx="10")
        btn_line = Button(root, text="直线", name="line")
        btn_line.pack(side="left", padx="10")
        btn_lineArrow = Button(root, text="直线(箭头)", name="lineArrow")
        btn_lineArrow.pack(side="left", padx="10")
        btn_color = Button(root, text="颜色", name="chooseColor")
        btn_color.pack(side="left", padx="10")
        # 给所有按钮处理事件
        btn_pen.bind_class("Button", "<1>", self.myEventManager)

        #为右键绑定事件
        root.bind("<Button-3>",self.createContextMenu)

        #程序一进来默认就处理鼠标拖动事件，默认使用画笔画画
        self.drawpad.bind("<B1-Motion>", self.myDrawPen)
        self.drawpad.bind("<ButtonRelease-1>", self.stopDraw)

        #增加快捷键处理
        root.bind("<KeyPress-r>", self.kuaijiejian)
        root.bind("<KeyPress-g>", self.kuaijiejian)
        root.bind("<KeyPress-y>", self.kuaijiejian)


    def myEventManager(self,event):
        name = event.widget.winfo_name()
        self.drawpad.bind("<ButtonRelease-1>", self.stopDraw)

        if name == "rect":
            self.drawpad.bind("<B1-Motion>", self.myDrawRect)
        elif name == "clear":
            self.drawpad.delete("all")
        elif name == "eraser":
            self.drawpad.bind("<B1-Motion>", self.myEraser)
        elif name == "line":
            self.drawpad.bind("<B1-Motion>", self.myLine)
        elif name == "lineArrow":
            self.drawpad.bind("<B1-Motion>", self.myLineArrow)
        elif name == "chooseColor":
            c = askcolor(color=self.fgcolor, title="选择画笔颜色")
            #print(c)  # ((225.87890625, 3.01171875, 30.1171875), '#e1031e')
            self.fgcolor = c[1]
        else:  # 画笔
            self.drawpad.bind("<B1-Motion>", self.myDrawPen)

    def createContextMenu(self,event):
        # 菜单在鼠标右键单击的坐标处显示
        self.contextMenu.post(event.x_root, event.y_root)

    def myDrawPen(self,event):

        #print("鼠标位置(相对于父容器)：({0},{1})".format(event.x, event.y))
        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x = event.x; self.y=event.y

        self.lastDraw = self.drawpad.create_line(self.x,self.y,event.x,event.y,fill=self.fgcolor)
        self.x = event.x
        self.y = event.y

    def stopDraw(self,event):
        self.startDrawFlag = False
        print("不能画")
        self.lastDraw = 0

    def myDrawRect(self,event):

        self.drawpad.delete(self.lastDraw)

        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x = event.x; self.y=event.y

        self.lastDraw = self.drawpad.create_rectangle(self.x,self.y,event.x,event.y,outline=self.fgcolor)

    def myEraser(self,event):
        if not self.startDrawFlag:
            self.startDrawFlag = True

        self.drawpad.create_rectangle(event.x - 4, event.y - 4, event.x + 4, event.y + 4,
                                      outline=self.bgcolor,fill=self.bgcolor)

    def myLine(self,event):
        self.drawpad.delete(self.lastDraw)

        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x = event.x; self.y=event.y

        self.lastDraw = self.drawpad.create_line(self.x, self.y, event.x, event.y,
                                                 fill=self.fgcolor)

    def myLineArrow(self,event):
        self.drawpad.delete(self.lastDraw)

        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x = event.x
            self.y=event.y

        self.lastDraw = self.drawpad.create_line(self.x, self.y, event.x, event.y,
                                                 fill=self.fgcolor,arrow=LAST)

    #处理快捷键
    def kuaijiejian(self,event):
        if event.char == "r":
            self.fgcolor = "#ff0000"
        elif event.char =="g":
            self.fgcolor = "#00ff00"
        elif event.char == "y":
            self.fgcolor = "#ffff00"


if __name__ == '__main__':
    root = Tk()
    root.geometry(str(win_width)+"x"+str(win_height)+"+400+400")
    root.title("百战程序员的画图软件")
    app = Application(master=root)
    root.mainloop()