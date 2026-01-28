"""
Qwen Agent 学习指南
包含基本概念、安装方法、使用示例和高级功能
"""

# 1. 基本概念和架构
"""
Qwen-Agent 是一个用于开发大语言模型（LLM）应用的框架，它基于通义千问（Qwen）模型的指令遵循、
工具使用、规划和记忆能力。该框架提供了一些示例应用，如浏览器助手、代码解释器和自定义助手。

核心特性：
1. 工具调用能力：Qwen-Agent 具有内置的函数调用功能，可以自动选择并调用适当的工具
2. 模型集成：支持接入阿里云 DashScope 服务提供的 Qwen 模型，也支持自部署 OpenAI 兼容的 API 服务
3. 模块化设计：提供原子组件（如 LLM 和工具）以及高级组件（如 Agent）
4. 多场景应用：可用于智能客服、数据分析、知识问答、多步骤任务处理等

架构组成：
- LLM 组件：继承自 BaseChatModel 类，具有函数调用能力
- 工具组件：继承自 BaseTool 类，提供特定功能
- 代理组件：继承自 Agent 类，协调 LLM 和工具的交互
"""

# 2. 安装方法
"""
1. 安装稳定版本：
   pip install -U qwen-agent

2. 安装带有可选功能的版本：
   pip install -U "qwen-agent[rag,code_interpreter,gui,mcp]"

3. 从源码安装：
   git clone https://github.com/QwenLM/Qwen-Agent.git
   cd Qwen-Agent
   pip install -e ./

4. 安装 GUI 支持（如果需要图形界面）：
   pip install -U qwen-agent[gui]
   # 或者从源码安装 GUI 支持
   pip install -e ./[gui]
"""

# 3. 基本使用方法示例

import os
import requests
from qwen_agent import Agent
from qwen_agent.tools.base import register_tool


@register_tool
def get_weather(city: str) -> str:
    """
    使用 wttr.in 查询天气的简单示例工具。
    """
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=3", timeout=8)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        # 捕获异常并返回字符串，避免中断 agent
        return f"查询失败: {exc}"


def build_simple_agent():
    """
    创建并返回一个简单的 Agent。
    """
    return Agent(
        model="qwen-max",  # 可换为 qwen-turbo 或自建的 OpenAI 兼容模型名
        api_key=os.getenv("QWEN_API_KEY"),
        temperature=0.3,
        system_prompt="你是乐于助人的助手。",
    )


def build_agent_with_tools():
    """
    创建并返回一个带工具的 Agent。
    """
    return Agent(
        model="qwen-max",  # 可换为 qwen-turbo 或自建的 OpenAI 兼容模型名
        api_key=os.getenv("QWEN_API_KEY"),
        temperature=0.3,
        tools=[get_weather],
        system_prompt="你是乐于助人的助手，会在需要时调用工具。",
    )


def simple_chat_example():
    """
    简单对话示例
    """
    agent = build_simple_agent()
    response = agent.run("用三句话介绍一下量子计算")
    print("简单对话示例:")
    print(response)


def tool_usage_example():
    """
    工具调用示例
    """
    agent = build_agent_with_tools()
    reply = agent.run("查一下北京今天的天气")  # Agent 会自动决定是否调用工具
    print("工具调用示例:")
    print(reply)


# 4. 高级功能示例

def advanced_assistant_example():
    """
    使用 Assistant 组件的高级功能示例
    """
    try:
        from qwen_agent.agents import Assistant
        
        # 配置 LLM 模型
        llm_cfg = {
            'model': 'qwen-max',
            'model_server': 'dashscope',  # 或者其他 OpenAI 兼容的服务
            'api_key': os.getenv("DASHSCOPE_API_KEY")
        }
        
        # 初始化助手
        bot = Assistant(llm=llm_cfg, system_message='你是一个有用的助手。')
        
        # 构建消息并运行
        messages = [{'role': 'user', 'content': '介绍一下杭州'}]
        print("高级 Assistant 示例:")
        for response in bot.run(messages):
            print(response)
    except ImportError:
        print("qwen-agent[rag] 或其他高级功能未安装，无法运行此示例")


def run_all_examples():
    """
    运行所有示例
    """
    print("=" * 50)
    print("Qwen Agent 学习指南 - 示例代码")
    print("=" * 50)
    
    # 简单对话示例
    if os.getenv("QWEN_API_KEY"):
        simple_chat_example()
    else:
        print("未设置 QWEN_API_KEY 环境变量，跳过简单对话示例")
    
    print("-" * 30)
    
    # 工具调用示例
    if os.getenv("QWEN_API_KEY"):
        tool_usage_example()
    else:
        print("未设置 QWEN_API_KEY 环境变量，跳过工具调用示例")
    
    print("-" * 30)
    
    # 高级功能示例
    if os.getenv("DASHSCOPE_API_KEY"):
        advanced_assistant_example()
    else:
        print("未设置 DASHSCOPE_API_KEY 环境变量，跳过高级功能示例")
    
    print("=" * 50)


if __name__ == "__main__":
    run_all_examples()