import os
# openai  组件没有安装
from openai import OpenAI

print(os.getenv("DASHSCOPE_API_KEY"))

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
#  固定的函数调用
completion = client.chat.completions.create(
    model="qwen-max",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    # message 表示用户输入内容  role表示我们和大模型扮演的角色  system 大模型身份  user 表示用户  assistant 助理
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': '你是谁？'}],
)

# print(completion.model_dump_json())
#  打印输出，completion大模型返回结果对象 . 导航访问属性     对象.属性
print(completion.choices[0].message.content)