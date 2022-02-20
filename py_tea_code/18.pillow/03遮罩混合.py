from PIL import Image
img1=Image.open('blend1.jpg')
img2=Image.open('blend2.jpg')
img2=img2.resize(img1.size)
r,g,b=img2.split()
Image.composite(img2,img1,b).show()