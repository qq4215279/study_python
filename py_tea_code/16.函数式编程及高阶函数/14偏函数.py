print(int('12345')) #将字符串按十进制转换为整数
print('转换为八进制：',int('12345',base=8))
print('转换为十六进制：',int('12345',16))
#将'1010' 按二进制转换为整数
print(int('1010',base=2))
print(int('101010',base=2))
print(int('10101010',base=2))
#定义函数
def new_int(s):
    return int(s,base=2)
print(new_int('1010'))
print(new_int('101010'))
print(new_int('10101010'))

from functools import partial
new_int=partial(int,base=2)
print(new_int('1010'))
print(new_int('101010'))
print(new_int('10101010'))
