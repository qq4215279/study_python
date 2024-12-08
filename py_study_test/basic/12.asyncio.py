# encoding: utf-8

import asyncio
import time

"""
asyncio 是 Python 标准库中的一个模块，专门用于编写异步 I/O 操作的代码。
它基于协程模型，允许开发者使用 async 和 await 关键字来编写非阻塞的代码，从而实现高效的并发执行。
asyncio 提供了事件循环、任务管理、网络 I/O、进程间通信等多种功能，非常适合处理 I/O 密集型和高并发的应用场景。

主要特性
1. 协程：使用 async def 定义的函数称为协程，可以使用 await 关键字来暂停执行，等待其他异步操作完成。
2. 事件循环：asyncio 的核心是事件循环，它负责调度和执行协程。事件循环会监控 I/O 操作，并在 I/O 准备好时唤醒相应的协程。
    eg: 使用 asyncio.run() 来运行一个协程，并自动管理事件循环。
3. 任务：使用 asyncio.create_task() 可以将协程包装成任务，使其在事件循环中并发运行。
    eg: 通过 asyncio.create_task() 创建任务，允许多个协程并发执行。
4. 并发执行：可以通过 asyncio.gather() 同时运行多个协程，并收集它们的结果。
    eg: asyncio.gather()   
5. 异步 I/O：asyncio 提供了异步版本的 socket、HTTP 客户端、文件 I/O 等操作，支持非阻塞 I/O。
    eg: asyncio 可以与其他库一起使用，例如 aiohttp，进行异步 HTTP 请求
6. 异常处理。在使用 asyncio 时，异常处理与同步编程类似，但需要在协程中进行处理：
7. 定时器：可以使用 asyncio.sleep() 创建非阻塞的延迟。


常用api:
1. 事件循环管理
    1.1. asyncio.run(func)  运行给定的协程，并管理事件循环的创建和关闭。它会阻塞直到协程完成。
    1.2. asyncio.get_event_loop()  获取当前线程的事件循环。如果没有，则会创建一个新的事件循环。eg: loop = asyncio.get_event_loop()
    1.3. asyncio.set_event_loop()  设置当前线程的事件循环。eg: asyncio.set_event_loop(loop)

2. 协程与任务
   2.1. asyncio.create_task()  将协程包装为任务，并将其调度到事件循环中。返回一个 Task 对象。eg: task = asyncio.create_task(some_coroutine())
   2.2. asyncio.gather()  并发运行多个协程，等待它们全部完成，并返回结果的列表。eg: results = await asyncio.gather(coroutine1(), coroutine2())
   2.3. asyncio.wait()  等待多个任务完成，返回一个包含完成和未完成任务的集合。eg: done, pending = await asyncio.wait({task1, task2})
   2.4. asyncio.shield()  保护某个任务不被取消。eg: await asyncio.shield(some_task())
   
3. 异步 I/O 操作
    3.1. asyncio.sleep()  非阻塞地等待指定的时间（以秒为单位）。eg: await asyncio.sleep(1)  # 等待 1 秒
    3.2. asyncio.open_connection()  创建一个 TCP 客户端连接，返回一个协议和流的元组。eg: reader, writer = await asyncio.open_connection('localhost', 8888)
    3.3. asyncio.start_server()  启动一个 TCP 服务器，返回一个服务器对象。eg: server = await asyncio.start_server(handle_client, 'localhost', 8888)

4. 取消与超时
    4.1. asyncio.Task.cancel()  取消一个任务。eg: task.cancel()
    4.2. asyncio.wait_for()  等待一个协程完成，并设置超时时间。如果超时，则抛出 asyncio.TimeoutError。eg: result = await asyncio.wait_for(some_coroutine(), timeout=5)
    
5. 其他实用函数
    5.1. asyncio.run_until_complete()  在事件循环中运行一个协程，直到它完成。eg: loop.run_until_complete(my_coroutine())
    5.2. asyncio.as_completed()  接受一个可迭代的任务，并返回一个迭代器，按完成顺序返回结果。
            for completed in asyncio.as_completed([task1(), task2()]):
                result = await completed
"""



# 1. 定义协程
async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # 模拟网络请求
    return "Data fetched"

def sync_fetch_data():
    print("Fetching data2...")
    # time.sleep(2)  # 模拟网络请求
    return "Data2 fetched"

async def main():
    print("Start")
    data = await fetch_data()  # 等待 fetch_data 完成
    print(data)
    print("-------------->")
    data2 = sync_fetch_data()  # 等待 fetch_data 完成
    print(data2)
    print("End")


# 2. 使用协程
print("start使用协程: ")
asyncio.run(main())
print("end 使用协程======================================>")


# 3. 创建任务
async def task1():
    await asyncio.sleep(1)
    print("Task 1 completed")

async def task2():
    await asyncio.sleep(2)
    print("Task 2 completed")

async def main_task():
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())
    await t1
    await t2

asyncio.run(main_task())


# 4. 可以同时运行多个协程并收集结果：
async def fetch_data_x(x):
    await asyncio.sleep(x)
    return f"Data {x}"

async def main_gather():
    results = await asyncio.gather(fetch_data_x(1), fetch_data_x(2), fetch_data_x(3))
    print(results)

asyncio.run(main_gather())


# 5. 异步网络请求
# asyncio 可以与其他库一起使用，例如 aiohttp，进行异步 HTTP 请求：
import aiohttp

async def fetch_http(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main_http():
    html = await fetch_http('https://example.com')
    print(html)

asyncio.run(main())


# 6. 异常处理
# 在异步编程中，异常处理与同步编程类似，但需要在协程中进行处理：
async def faulty_task():
    raise ValueError("An error occurred")

async def main_except():
    try:
        await faulty_task()
    except ValueError as e:
        print(f"Caught an exception: {e}")

asyncio.run(main_except())