from distutils.core import setup

setup(
    name='baizhanSuperMath',  # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，用于测试哦',  #描述
    author='gaoqi', # 作者
    author_email='gaoqi110@163.com',
    py_modules=['baizhanSuperMath.demo1','baizhanSuperMath.demo2'] # 要发布的模块
)
