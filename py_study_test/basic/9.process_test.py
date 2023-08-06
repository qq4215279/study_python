# encoding: utf-8
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Manager

import os
import time

"""
进程
进程的创建 process = Process([group [, target [, name [, args [, kwargs]]]]])  
    其中：target 表示调用对象；args 表示调用对象的位置参数元组；kwargs 表示调用对象的字典；name 为进程别名；group 参数未使用，值始终为None。

api：
    process.is_alive()  如果p仍然运行，返回True
    process.join([timeout])  等待进程p终止。Timeout是可选的超时期限，进程可以被链接无数次，但如果连接自身则会出错
    process.run()  进程启动时运行的方法。默认情况下，会调用传递给Process构造函数的target。定义进程的另一种方法是继承Process类并重新实现run()函数
    process.start()	 启动进程，这将运行代表进程的子进程，并调用该子进程中的run()函数
    process.terminate() 	强制终止进程。如果调用此函数，进程p将被立即终止，同时不会进行任何清理动作。如果进程p创建了它自己的子进程，这些进程将变为僵尸进程。使用此方法时需要特别小心。如果p保存了一个锁或参与了进程间通信，那么终止它可能会导致死锁或I/O损坏
    process.name  进程的名称
    process.pid	 进程的整数进程ID


进程池
在利用Python进行系统管理的时候，特别是同时操作多个文件目录，或者远程控制多台主机，并行操作可以节约大量的时间。
当被操作对象数目不大时，可以直接利用multiprocessing中的Process动态成生多个进程，十几个还好，但如果是上百个，上千个目标，手动的去限制进程数量却又太过繁琐，此时可以发挥进程池的功效。
Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；
但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程。
进程池创建  pool = Pool([numprocess [, initializer [, initargs]]]) 
    其中: numprocess 是要创建的进程数,如果省略此参数，将使用cpu_count()的值；Initializer 是每个工作进程启动时要执行的可调用对象；
         Initargs 是要传递给initializer的参数元祖，Initializer默认为None。

api：
    apply(func [,args [,kwargs]])  在一个池工作进程中执行函数（*args，**kwargs），然后返回结果。阻塞！
    apply_async(func [, args [,kwargs [,callback ] ] ])  在一个池工作进程中异步地执行函数（*args，**kwargs），然后返回结果。
            此方法的结果是AsyncResult类的实例，稍后可用于获得最终结果。Callback是可调用对象，接受输入参数。当func的结果变为可用时，将立即传递给callback。
            Callback禁止执行任何阻塞操作，否则将阻塞接收其他异步操作中的结果。非阻塞！
    close()  关闭进程池，防止进行进一步操作。如果还有挂起的操作，它们将在工作进程终止之前完成
    join()  等待所有工作进程退出。此方法只能在close() 或者terminate() 方法之后调用
    imap(func, iterable [ ,chunksize])	map() 函数的版本之一，返回迭代器而非结果列表
    imap_unordered(func, iterable [, chunksize])  同 imap() 函数一样，只是结果的顺序根据从工作进程接收到的时间任意确定
    map(func, iterable [, chunksize])  将可调用对象func应用给iterable中的所有项，然后以列表的形式返回结果。通过将iterable划分为多块并将工作分派给工作进程，可以并行地执行这项操作。
            chunksize指定每块中的项数。如果数量较大，可以增大chunksize的值来提升性能
    map_async(func, iterable [, chunksize [, callback]] )	同 map() 函数，但结果的返回是异步的。返回值是AsyncResult类的实例，稍后可用与获取结果。
            Callback是指接受一个参数的可调对象。如果提供callable，当结果变为可用时，将使用结果调用callable
    terminate()  立即终止所有工作进程，同时不执行任何清理或结束任何挂起工作。如果p被垃圾回收，将自动调用此函数
    get([timeout])	返回结果，如果有必要则等待结果到达。Timeout是可选的超时。如果结果在指定时间内没有到达，将引发multiprocessing.TimeoutError异常。
            如果远程操作中引发了异常，它将在调用此方法时再次被引发
    ready()	如果调用完成，则返回True
    sucessful()	 如果调用完成且没有引发异常，返回True。如果在结果就绪之前调用此方法，将引发AssertionError异常
    wait([timeout])  等待结果变为可用。Timeout是可选的超时


进程间通信。全局变量在多个进程中不共享，进程之间的数据是独立的，默认情况下互不影响。
Queue 是多进程安全的队列，可以使用Queue实现多进程之间的数据传递。
创建：queue = Queue(size)
api：
    put(item [, block [, timeout]])  将item放入队列。如果队列已满，此方法将阻塞至有空间可用为止。
        block控制阻塞行为，默认为True。如果设置为False，将引发Queue.Empty异常(定义在Queue模块中)；timeout指定在阻塞模式中等待可用时空间的时间长短。超时后将引发Queue.Full异常。
    get([block [,timeout])  返回queue中的一个项。如果queue为空，此方法将阻塞，直到队列中有项可用为止。
        block用于控制阻塞行为，默认为True。如果设置为False，将引发Queue.Empty异常(定义在Queue模块中)；timeout是可选超时时间，用在阻塞模式中。如果在指定的时间间隔内没有项变为可用，将引发Queue.Empty异常
    cancle_join_thread()  不会在进程退出时自动连接后台线程。这可以防止join_thread()方法阻塞
    qsize()	返回目前队列中项的正确数量。
    full()  如果queue已满，返回True
    empty()  如果调用此方法时queue为空，返回True
    task_done()  消费者使用此方法发出信号，表示 queue.get() 返回的项已经被处理。如果调用此方法的次数大于从队列中删除的项的数量，将引发ValueError异常
    join_thread()  连接队列的后台线程。此方法用于在调用 queue.close() 方法之后，等待所有队列项被消耗。默认情况下此方法由不是queue的原始创建者的所有进程调用。调用queue.cancle_join_thread()方法可以禁止这种行为
    joinableQueue([maxsize])  创建可连接的共享进程队列。这就像是一个Queue对象，但队列允许项的消费者通知生产者项已经被成功处理。通知进程是使用共享的信号和条件变量来实现的
    join()  生产者使用此方法进行阻塞，知道队列中的所有项均被处理。阻塞将持续到位队列中的每个项均调用queue.task_done()方法为止
    close()  关闭队列，防止队列中加入更多数据。调用此方法时，后台线程将继续写入那些已入队列尚未写入数据，但将在此方法完成时马上关闭

注意： 如果使用Pool创建进程，就需要使用multiprocessing.Manager()中的Queue()来完成进程间的通信，而不是 multiprocessing.Queue()，
    # 否则会抛出如下异常: RuntimeError: Queue objects should only be shared between processes through inheritance
创建：queue = multiprocessing.Manager().Queue(size)
"""


# 进程使用方式1：定义子进程代码，并传递参数
def run_proc(name, age, interval, **kwargs):
    for i in range(5):
        print('子进程运行中，参数name：%s,age:%d' % (name, age))
        print('字典参数kwargs：', kwargs)
        time.sleep(interval)


# 进程使用方式2：定义线程类
class ClockProcess(Process):
    def __init__(self, interval):
        Process.__init__(self)
        self.interval = interval

    def run(self):
        print('子进程开始执行的时间:{}'.format(time.ctime()))
        time.sleep(self.interval)
        print('子进程结束的时间:{}'.format(time.ctime()))

# 写
def write(queue):
    # 将列表中的元素写入队列中
    for i in ["a", "b", "c"]:
        print('开始写入值%s' % i)
        print('消息队列是否已满：', queue.full())

        # 因为消息队列已满，需要直接写入需要等待，如果超时会抛出异常，所以写入时候需判断，消息队列是否已满
        if not queue.full:
            queue.put(i)

        time.sleep(1)


# 读取
def read(queue):
    print('开始读取')
    while True:
        # 同理读取消息时，先判断消息队列是否为空，再读取
        if not queue.empty():
            print('读取到:', queue.get())
            time.sleep(1)
        else:
            break


if __name__ == '__main__':
    # 1. 进程的使用方式1：
    '''
    print('主进程开始运行')
    p = Process(target=run_proc, args=('test', 18, 5), kwargs={'m': 23})
    print('子进程将要执行')
    p.start()
    # 等待进程p终止
    p.join()
    # join()方法中加超时的使用
    # p.join(3)

    # 获取进程的ID
    print('p.id: ', p.pid)
    # 获取进程的名称
    print('p.name: ', p.name)
    # 判断进程是否运行
    print('p.is_alive: ', p.is_alive())
    print("主进程结束!")
    print("进程使用方式1 end ------------------------------>")
    '''

    # 2. 进程的使用方式2：
    '''
    # 创建进程
    p2 = ClockProcess(2)
    # 启动进程
    p2.start()
    p2.join()
    print('主进程结束')
    print("进程使用方式2 end ------------------------------>")
    '''

    # 3. 进程池的使用
    '''
    pool = Pool(processes=3)
    for i in range(5):
        msg = "hello %d" % (i)
        # 非阻塞进程！维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        pool.apply_async(run_proc, (msg, i, 3))

        # 阻塞进程！维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
        # pool.apply(run_proc, (msg, i, 3))

    pool.close()  # 进程池关闭之后不再接收新的请求
    # 调用join之前，先调用close函数，否则会出错。
    # 执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    pool.join()
    '''

    # 4.1 Queue 使用
    '''
    # 创建队列
    queue = Queue()
    # 创建写入进程
    # 注：如果使用Pool创建进程，就需要使用multiprocessing.Manager()中的Queue()来完成进程间的通信，而不是multiprocessing.Queue()，
    # 否则会抛出如下异常: RuntimeError: Queue objects should only be shared between processes through inheritance
    pw = Process(target=write, args=(queue,))
    pr = Process(target=read, args=(queue,))
    # 启动进程
    pw.start()
    pw.join()
    pr.start()
    pr.join()
    '''

    # 4.2 multiprocessing.Manager().Queue() 使用
    '''
    # 创建队列
    queue2 = Manager().Queue()
    # 创建进程池
    pool2 = Pool(3)
    # 使用阻塞模式创建进程
    pool2.apply(write, (queue2,))
    pool2.apply(read, (queue2,))
    pool2.close()
    pool2.join()
    '''