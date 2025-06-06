# encoding: utf-8

# print('\n'.join([line for line in [''.join([('Love'[(x - y) % len('Love')] if ((x * 0.05) ** 2 + (
#             y * 0.1) ** 2 - 1) ** 3 - (x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in
#                                    range(30, -30, -1)] if
#                  line != '                                                            ']))

import turtle
import time


# 画心形圆弧
def hart_arc():
    for i in range(200):
        turtle.right(1)
        turtle.forward(2)


def move_pen_position(x, y):
    turtle.hideturtle()  # 隐藏画笔（先）
    turtle.up()  # 提笔
    turtle.goto(x, y)  # 移动画笔到指定起始坐标（窗口中心为0,0）
    turtle.down()  # 下笔
    turtle.showturtle()  # 显示画笔


love = input("请输入表白话语，默认为‘I Love You’：")
signature = input("请签署你的大名，不填写默认不显示：")

if love == '':
    love = 'I Love You'

time.sleep(1)

# 初始化
turtle.setup(width=800, height=500)  # 窗口（画布）大小
turtle.color('red', 'pink')  # 画笔颜色
turtle.pensize(3)  # 画笔粗细
turtle.speed(1)  # 描绘速度
# 初始化画笔起始坐标
move_pen_position(x=0, y=-180)  # 移动画笔位置
turtle.left(140)  # 向左旋转140度

turtle.begin_fill()  # 标记背景填充位置

# 画心形直线（ 左下方 ）
turtle.forward(224)  # 向前移动画笔，长度为224
# 画爱心圆弧
hart_arc()  # 左侧圆弧
turtle.left(120)  # 调整画笔角度
hart_arc()  # 右侧圆弧
# 画心形直线（ 右下方 ）
turtle.forward(224)

turtle.end_fill()  # 标记背景填充结束位置

# 在心形中写上表白话语
move_pen_position(0, 0)  # 表白语位置
turtle.hideturtle()  # 隐藏画笔
turtle.color('#CD5C5C', 'pink')  # 字体颜色
# font:设定字体、尺寸（电脑下存在的字体都可设置）  align:中心对齐
turtle.write(love, font=('Arial', 30, 'bold'), align="center")

# 签写署名
if signature != '':
    turtle.color('red', 'pink')
    time.sleep(2)
    move_pen_position(180, -180)
    turtle.hideturtle()  # 隐藏画笔
    turtle.write(signature, font=('Arial', 20), align="center")

# 点击窗口关闭程序
window = turtle.Screen()
window.exitonclick()