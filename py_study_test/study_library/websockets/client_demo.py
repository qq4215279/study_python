# encoding: utf-8

import asyncio
import websockets


# 保持心跳
async def keep_alive(websocket):
    try:
        while True:
            await websocket.ping()  # 发送 Ping 消息
            await asyncio.sleep(30)  # 每 30 秒发送一次
    except Exception as e:
        print(f"Keep alive error: {e}")
        # 当心跳异常时，通知客户端断开连接
        await websocket.send("Server: Connection lost, closing.")
        await websocket.close()  # 主动关闭连接


async def echo():
    async with websockets.connect("ws://localhost:8765") as websocket:
        # test1
        # await websocket.send("Hello, Server!")
        # response = await websocket.recv()
        # print(f"Received from server: {response}")

        # test_baloot
        # 创建一个独立的任务来运行 keep_alive
        asyncio.create_task(keep_alive(websocket))

        async for message in websocket:
            print(f"Received: {message}")
            await websocket.send(f"Echo: {message}")


asyncio.get_event_loop().run_until_complete(echo())
