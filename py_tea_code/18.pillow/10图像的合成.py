from PIL import Image,ImageChops
#打开图片
img1=Image.open('blend1.jpg')
img2=Image.open('blend2.jpg')
#对两张图片进行算术加法运算
# ImageChops.add(img1,img2).show()

#对两张图片进行算术减法运算
# ImageChops.subtract(img1,img2).show()

#使用darker()函数
# ImageChops.darker(img1,img2).show()

#变亮函数lighter()函数
# ImageChops.lighter(img1,img2).show()

#两张图片相互叠加multiply
# ImageChops.multiply(img1,img2).show()

#sreen()
# ImageChops.screen(img1,img2).show()

#反色invert()
# ImageChops.invert(img1).show()

#比较函数difference()
ImageChops.difference(img2,img2).show()