'''
 map(func, *iterables) --> map object

    Make an iterator that computes the function using arguments from
    each of the iterables.  Stops when the shortest iterable is exhausted.
'''
a=[1,2,3,4]
b=[10,20,30]
def f(x,y):
    return x+y
L=map(f,a,b)
print(list(L))

