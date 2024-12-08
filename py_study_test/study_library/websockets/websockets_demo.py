# encoding: utf-8

import asyncio
import websockets

"""
websockets 是一个用于在 Python 中实现 WebSocket 客户端和服务器的库。它提供了一组简单而强大的 API，使得创建和管理 WebSocket 连接变得容易。

相关api: 
1. websockets.serve(handler, host, port, **options)  创建一个 WebSocket 服务器。
    handler: 处理 WebSocket 连接的协程函数，通常接收两个参数：websocket（客户端连接）和 path（请求路径）。
    host: 服务器主机名（例如 "localhost"）。
    port: 服务器端口号（例如 8765）。
    options: 其他可选参数，例如 max_size（最大消息大小）、ping_interval（ping 间隔）等。
    
2. websockets.connect(uri, **options)  这个函数用于创建 WebSocket 客户端连接。    
    uri: WebSocket 服务器的 URI（例如 "ws://localhost:8765"）。
    options: 其他可选参数，例如 subprotocols（支持的子协议列表）。

3. websocket.send(message):  发送消息到 WebSocket 服务器。

4. websocket.recv(): 接收来自 WebSocket 服务器的消息。此方法是一个协程，返回收到的消息。

5. websocket.close()  关闭 WebSocket 连接。

6. websocket.open  检查连接是否仍然打开。

7. websockets.exceptions.ConnectionClosed  当连接关闭时，会抛出此异常。你可以捕获此异常以处理连接关闭的情况。

其他功能
Ping/Pong 机制: websockets 库会自动处理 ping/pong 机制，你可以通过设置 ping_interval 来控制 ping 的发送频率。
自定义子协议: 在连接时可以指定支持的子协议。
"""


# 1. 创建一个 WebSocket 服务器。
async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)

start_server = websockets.serve(echo, "localhost", 8765)

# 2. 创建 WebSocket 客户端连接。
async with websockets.connect("ws://localhost:8765") as websocket:
    await websocket.send("Hello, Server!")
    response = await websocket.recv()
    print(f"Received from server: {response}")



def catch_close_exception():
    try:
        async for message in websocket:
            print(message)
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")