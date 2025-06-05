from concurrent.futures import ThreadPoolExecutor, as_completed
import time

"""
websocket-client
websockets
"""

"""
使用线程池执行线程任务步骤
1. 调用 ThreadPoolExecutor(max_workers=3) 类的构造器创建一个线程池。
2. 定义一个普通函数作为线程任务。
3. 调用 ThreadPoolExecutor 对象的 submit() 方法提交线程任务。
4. 当不想提交任何任务时，调用 ThreadPoolExecutor 对象的 shutdown() 方法来关闭线程


api:
ThreadPoolExecutor(max_workers=3) as executor ：最多同时运行3个线程。
executor.submit(func, *args)： 提交单个任务，返回一个Future对象（代表异步操作的结果）
as_completed(futures)：返回已完成任务的 Future 对象的迭代器。
future.result()：按任务完成顺序获取结果
executor.shutdown(wait=True)  用于关闭线程池并释放资源。参数 wait=True（默认）表示‌阻塞等待所有任务完成后再关闭‌；
                                若设置为 wait=False，则直接关闭线程池，但未完成的任务会继续执行（需手动管理后续等待）；如果使用 with 语句，无需手动调用 shutdown()。

executor.map() 批量提交任务，按顺序返回结果
"""


# 创建包含4个线程的线程池
# 使用 with ThreadPoolExecutor() as executor 时，会在代码块结束时自动调用 shutdown(wait=True)，无需手动操作


def task(n):
    time.sleep(1)
    return f"Task {n} completed"


# 创建线程池，最多运行3个线程
with ThreadPoolExecutor(max_workers=4) as executor:
    # 方式1：
    # 提交多个任务
    futures = [executor.submit(task, i) for i in range(5)]

    # 获取每个任务的返回结果
    for future in as_completed(futures):
        result = future.result()
        print(result)

    # 方式2：
    # results = executor.map(task, range(5))



# ==================================================>
print("==================================================>")

# 定义两个任务函数
def task_a(n):
    time.sleep(1)
    return f"A: {n}"

def task_b(n):
    time.sleep(1)
    return f"B: {n}"

# 初始化线程池组（2个不同的线程池）
thread_pools = {
    "group_a": ThreadPoolExecutor(max_workers=2),
    "group_b": ThreadPoolExecutor(max_workers=3)
}

# 提交任务到不同的线程池
futures = []
for i in range(5):
    futures.append(thread_pools["group_a"].submit(task_a, i))
    futures.append(thread_pools["group_b"].submit(task_b, i))

# 获取任务结果
for future in as_completed(futures):
    print(future.result())

# 记得关闭线程池
for pool in thread_pools.values():
    pool.shutdown(wait=True)