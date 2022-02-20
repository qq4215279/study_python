from PIL import Image
img=Image.open('bjsxt.png')
#图像的旋转
# img.rotate(180).show()

#格式转换
# img.transpose(Image.FLIP_TOP_BOTTOM).show() # 上下滤镜
# img.transpose(Image.FLIP_LEFT_RIGHT).show() # 左右滤镜
# img.transpose(Image.ROTATE_90).show() # 90滤镜
# img.transpose(Image.ROTATE_180).show() # 180滤镜
img.transpose(Image.TRANSPOSE).show() # 颠倒滤镜