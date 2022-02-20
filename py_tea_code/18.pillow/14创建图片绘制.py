from PIL import Image,ImageDraw,ImageFont
#创建一幅白色背景的图像
img=Image.new('RGB',(300,300),'white')

#绘制一个矩形
draw_obj=ImageDraw.Draw(img)
draw_obj.rectangle((50,50,280,200),fill='blue',outline='red')
# draw_obj.text((80,80),'bjsxt',fill='green')
font=ImageFont.truetype('SIMLI.TTF',20)
draw_obj.text((80,80),'北京尚学堂',font=font,fill='white')
img.show()
