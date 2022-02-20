from PIL import Image
#按像素缩放图片
img1= Image.open('bjsxt.png')
# img1.show()
#.将每个像素都扩大2倍
# Image.eval(img1,lambda x:x*2).show()

#按尺寸进行缩放图片
#复制图片
img2=img1.copy()
print(img2.size)
img1.show()
img2.thumbnail((200,160))
img2.show()