# encoding: utf-8

import random

"""
random 模块
random 模块是 Python 标准库中的一个模块，提供了生成随机数的功能。它可以用于生成随机数、随机选择元素、打乱序列等各种与随机性相关的操作。

api: 
    randint(a, b)  生成一个介于 a 和 b 之间的整数，包括 a 和 b。
    random()  生成一个0到1之间的随机浮点数。
    uniform(a, b)  生成一个在范围 a 到 b 之间的随机浮点数。
    choice(seq)  从序列 seq 中随机选择一个元素并返回。
    randrange(start, stop[, step])  生成一个在指定范围内的随机整数，start 是范围的起始值，stop 是范围的结束值（不包括在内），step 是步长。
    sample(population, k)  从 population 中随机选择 k 个不重复的元素，返回一个列表。
    shuffle(seq)  打乱序列 seq 中的元素的顺序，改变原始序列。

    seed(a=None)  初始化随机数生成器的种子。如果不提供 a，则使用系统时间作为种子。
    random.getrandbits(k)  生成 k 个随机的比特位，返回一个整数。
    random.expovariate(lambd)  生成一个指数分布的随机浮点数，参数 lambd 是指数分布的参数。
    random.gauss(mu, sigma)  生成一个服从高斯分布（正态分布）的随机浮点数，mu 是均值，sigma 是标准差。
    random.choices(population, weights=None, cum_weights=None, k=1)  从 population 中根据权重随机选择 k 个元素，返回一个列表。
    random.betavariate(alpha, beta)  生成一个贝塔分布的随机浮点数，参数 alpha 和 beta 是贝塔分布的参数。
    random.paretovariate(alpha)  生成一个帕累托分布的随机浮点数，参数 alpha 是分布的形状参数。    
"""


def random_test():
    print("范围整数: ", random.randint(1, 2))
    print("0-1随机浮点数: ", random.random())
    print("范围随机浮点数: ", random.uniform(1, 4))
    fruits = ['apple', 'banana', 'cherry', 'date']
    print("随机选择一个元素: ", random.choice(fruits))
    print("指定范围内的随机整数: ", random.randrange(1, 10, 2))
    print("随机选择 k 个不重复的元素: ", random.sample((1, 4, 55, 100, 999), 3))
    random.shuffle(fruits)
    print("打乱列表中的元素顺序: ", fruits)



if __name__ == '__main__':
    random_test()