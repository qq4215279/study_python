# encoding: utf-8

import threading
from queue import Queue
import time

"""
线程
线程也是实现多任务的一种方式，一个进程中，也经常需要同时做多件事，就需要同时运行多个‘子任务’，这些子任务就是线程。一个进程可以拥有多个并行的线程，其中每一个线程，共享当前进程的资源。

进程和线程在使用上各有优缺点：线程执行开销小，但不利于资源的管理和保护，而进程正相反。具体区别如下：
区别	                                进程	                                                                线程
根本区别	                        作为资源分配的单位	                                                     调度和执行的单位
开销	            每一个进程都有独立的代码和数据空间，进程间的切换会有较大的开销	            线程可以看出是轻量级的进程，多个线程共享内存，线程切换的开销小
所处环境	                在操作系统中，同时运行的多个任务	                                              在程序中多个顺序流同时执行
分配内存	            系统在运行的时候为每一个进程分配不同的内存区域	                                    线程所使用的资源是他所属进程的资源
包含关系	                    一个进程内可以拥有多个线程	                                    线程是进程的一部分，所有线程有时候称为是轻量级的进程

_thread 和 threading 提供对线程的支持。_thread 提供了低级别的、原始的线程以及一个简单的锁，它相比于 threading 模块的功能还是比较有限的。
threading 模块除了包含 _thread 模块中的所有方法外，还提供的其他方法：
threading.currentThread(): 返回当前的线程变量。
threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。
threading.activeCount(): 返回正在运行的线程数量，与 len(threading.enumerate())有相同的结果。


创建方式1: t = threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
    其中target: 要执行的方法；name: 线程名；args/kwargs: 要传入方法的参数。
创建方式2：通过继承类threading.Thread的方式来创建一个线程。
    这种方法只要重写类threading.Thread中的方法run()，然后再调用方法start()就能创建线程，并运行方法run()中的代码。    

api:
    run()  用以表示线程活动的方法
    start()  启动线程活动
    join([time])  等待至线程中止。这阻塞调用线程直至线程的 join() 方法被调用中止-正常退出或者抛出未处理的异常-或者是可选的超时发生
    isAlive()  返回线程是否活动的
    getName()  返回线程名
    setName()  设置线程名

线程共享全局变量
互斥锁：
    创建一把互斥锁 lock = threading.Lock()
    api：
         lock.acquire()  获取锁
         lock.lock  释放锁


生产者消费者模式

queue 模块
提供了线程安全的队列（Queue）实现，用于在多线程环境下进行线程间的数据通信。队列是一种常见的数据结构，用于存储和管理数据项，通常遵循先进先出（FIFO）的原则。
queue 模块提供了多种队列实现，包括以下几种：
    1. Queue: Queue 类是一个线程安全的队列实现，可用于在多线程环境下传递数据。它支持先进先出的操作。
        创建: queue = Queue()
        常用方法包括：
            put(item, block=True, timeout=None)：将元素放入队列，可设置是否阻塞和超时。
            get(block=True, timeout=None)：从队列中获取元素，可设置是否阻塞和超时。
            qsize()：返回队列中元素的数量。
            empty()：判断队列是否为空。
            full()：判断队列是否已满。
            
    2. LifoQueue: LifoQueue 类是一个线程安全的后进先出（LIFO）队列实现，与普通队列不同的是，它在尾部插入元素，并从尾部获取元素。

    3. PriorityQueue: PriorityQueue 类是一个线程安全的优先级队列实现，元素被插入队列时会根据优先级排序。
    
    
ThreadLocal
多线程环境下，每一个线程均可以使用所属进程的全局变量。如果一个线程对全局变量进行了修改，将会影响到其他所有的线程对全局变量的计算操作，从而出现数据混乱，即为脏数据。
为了避免多个线程同时对变量进行修改，引入了线程同步机制，通过互斥锁来控制对全局变量的访问。
所以有时候线程使用局部变量比全局变量好，因为局部变量只有线程自身可以访问，同一个进程下的其他线程不可访问。但是局部变量也是有问题，就是在函数调用的时候，传递起来很麻烦。
因此 Python 还提供了 ThreadLocal 变量，它本身是一个全局变量，但是每个线程却可以利用它来保存属于自己的私有数据，这些私有数据对其他线程也是不可见的。
创建全局ThreadLocal对象: local = threading.local()

"""

# 1. ---------------------------------------------------------->
def fun1(thread_name, delay):
    print('线程{0}开始运行fun1'.format(thread_name))
    time.sleep(delay)
    # print('线程{0}运行fun1结束'.format(thread_name))
    print('线程{0}运行fun1结束'.format(threading.current_thread().getName()))


def fun2(thread_name, delay):
    print('线程{0}开始运行fun2'.format(thread_name))
    time.sleep(delay)
    # print('线程{0}运行fun2结束'.format(thread_name))
    print('线程{0}运行fun2结束'.format(threading.current_thread().getName()))


# 2. ---------------------------------------------------------->
# 创建线程类继承 threading.Thread
class MyThread(threading.Thread):
    # 重写父类的构造方法，其中func是线程函数，args是传入线程的参数,name是线程名
    def __init__(self, func, name, args):
        super().__init__(target=func, name=name, args=args)

    # 重写父类的run()方法
    def run(self):
        self._target(*self._args)


def fun11(delay):
    print('线程{}执行fun11'.format(threading.current_thread().getName()))
    time.sleep(delay)
    print('线程{}执行fun11结束'.format(threading.current_thread().getName()))


def fun22(delay):
    print('线程{}执行fun22'.format(threading.current_thread().getName()))
    time.sleep(delay)
    print('线程{}执行fun22结束'.format(threading.current_thread().getName()))


# 3. ---------------------------------------------------------->
# 生产者线程
class Producer(threading.Thread):
    def run(self):
        global queue
        count = 0
        while True:
            if queue.qsize() < 1000:
                for i in range(100):
                    count += 1
                    msg = '生成产品' + str(count)
                    queue.put(msg)
                    print(msg)
            time.sleep(0.5)


# 消费者线程
class Consumer(threading.Thread):
    def run(self):
        global queue
        while True:
            if queue.qsize() > 100:
                for i in range(3):
                    msg = self.name + '消费了' + queue.get()
                    print(msg)
            time.sleep(1)

# 4. ---------------------------------------------------------->
# 创建全局ThreadLocal对象:
local = threading.local()


def process_student():
    # 获取当前线程关联的name:
    student_name = local.name
    print('线程名：%s 学生姓名:%s' % (threading.current_thread().name, student_name))


def process_thread(name):
    # 绑定ThreadLocal的name:
    local.name = name
    process_student()


if __name__ == '__main__':
    # 1. 线程创建方式1：
    # '''
    print('开始运行')
    # 创建线程
    t1 = threading.Thread(target=fun1, args=('thread-1', 2))
    t2 = threading.Thread(target=fun2, args=('thread-2', 4))
    t1.start()
    t2.start()
    # '''

    # 2. 线程创建方式2：
    '''
    print('开始运行')
    # 创建线程
    t11 = MyThread(fun11, 'thread-11', (2,))
    t22 = MyThread(fun22, 'thread-22', (4,))
    t11.start()
    t22.start()
    t11.join()
    t22.join()
    '''

    # 3. 生产者-消费者模型
    '''
    # 定义常量
    queue = Queue()
    p = Producer()
    p.start()
    time.sleep(1)
    c = Consumer()
    c.start()
    '''

    # 4. ThreadLocal的使用
    '''
    t41 = threading.Thread(target=process_thread, args=('张三',), name='Thread-A')
    t42 = threading.Thread(target=process_thread, args=('李四',), name='Thread-B')
    t41.start()
    t42.start()
    '''
