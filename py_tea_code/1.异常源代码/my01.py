# coding=utf-8
# Traceback追溯，追根溯源。most recent call last最后一次调用。

def a():
    num = 1/0

def b():
    a()

def c():
    b()


c()
