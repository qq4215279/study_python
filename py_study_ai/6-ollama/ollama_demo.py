import asyncio
import ollama
from ollama import generate
from ollama import chat
from ollama import ChatResponse
from ollama import Client
from ollama import AsyncClient

# 1. 对话模式
response = generate(
    model="deepseek-r1",  # 模型名称 deepseek-r1  llama3.2
    prompt="你是谁。"  # 提示文本
)
print("1. 对话模式 " + response)

# 2. 流式相应
stream = chat(
    model="deepseek-r1",
    messages=[{"role": "user", "content": "为什么天空是蓝色的？"}],
    stream=True
)
for chunk in stream:
    print("2. 流式相应 " + chunk["message"]["content"], end="", flush=True)


"""
3.1. 自定义客户端
你还可以创建自定义客户端，来进一步控制请求配置，比如设置自定义的 headers 或指定本地服务的 URL。

创建自定义客户端
通过 Client，你可以自定义请求的设置（如请求头、URL 等），并发送请求。
"""
print("3.1. 自定义客户端==========:")
client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

response = client.chat(model='deepseek-r1', messages=[
    {
        'role': 'user',
        'content': '你是谁?',
    },
])
print(response['message']['content'])



"""
3.2. 异步客户端
如果你希望异步执行请求，可以使用 AsyncClient 类，适用于需要并发的场景。
异步客户端支持与传统的同步请求一样的功能，唯一的区别是请求是异步执行的，可以提高性能，尤其是在高并发场景下。
"""
print("3.2. 异步客户端===>")
async def chat():
    message = {'role': 'user', 'content': '你是谁?'}
    response = await AsyncClient().chat(model='deepseek-r1', messages=[message])
    print(response['message']['content'])

asyncio.run(chat())




"""
3.3. 异步流式响应
如果你需要异步地处理流式响应，可以通过将 stream=True 设置为异步生成器来实现。
这里，响应将逐部分地异步返回，每部分都可以即时处理。
"""
print("3.3. 异步流式响应===>")
async def chat():
    message = {'role': 'user', 'content': '你是谁?'}
    async for part in await AsyncClient().chat(model='deepseek-r1', messages=[message], stream=True):
        print(part['message']['content'], end='', flush=True)
asyncio.run(chat())
