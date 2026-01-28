# Qwen Agent 学习教程

## 1. 概述

Qwen-Agent 是一个用于开发大语言模型（LLM）应用的框架，它基于通义千问（Qwen）模型的指令遵循、工具使用、规划和记忆能力。该框架提供了一些示例应用，如浏览器助手、代码解释器和自定义助手。

### 核心特性：

1. **工具调用能力**：Qwen-Agent 具有内置的函数调用功能，可以自动选择并调用适当的工具
2. **模型集成**：支持接入阿里云 DashScope 服务提供的 Qwen 模型，也支持自部署 OpenAI 兼容的 API 服务
3. **模块化设计**：提供原子组件（如 LLM 和工具）以及高级组件（如 Agent）
4. **多场景应用**：可用于智能客服、数据分析、知识问答、多步骤任务处理等

### 架构组成：

- **LLM 组件**：继承自 BaseChatModel 类，具有函数调用能力
- **工具组件**：继承自 BaseTool 类，提供特定功能
- **代理组件**：继承自 Agent 类，协调 LLM 和工具的交互

## 2. 安装方法

### 2.1 基础安装

```bash
pip install -U qwen-agent
```

### 2.2 带可选功能安装

```bash
# 安装带有 RAG、代码解释器、GUI 和 MCP 功能的版本
pip install -U "qwen-agent[rag,code_interpreter,gui,mcp]"
```

### 2.3 从源码安装

```bash
git clone https://github.com/QwenLM/Qwen-Agent.git
cd Qwen-Agent
pip install -e ./
```

### 2.4 GUI 支持安装

```bash
# 安装 GUI 支持
pip install -U qwen-agent[gui]

# 或者从源码安装 GUI 支持
pip install -e ./[gui]
```

## 3. 基本使用方法

### 3.1 简单对话示例

```python
from qwen_agent import Agent

# 初始化 Agent
agent = Agent(
    model="qwen-max",
    api_key=os.getenv("QWEN_API_KEY"),  # 也可以使用环境变量
    system_prompt="你是乐于助人的助手。"
)

# 简单对话
response = agent.run("用三句话介绍一下量子计算")
print(response)
```

### 3.2 工具调用示例

```python
import os
import requests
from qwen_agent import Agent
from qwen_agent.tools.base import register_tool

# 定义并注册工具
@register_tool
def get_weather(city: str) -> str:
    """使用 wttr.in 查询天气的简单示例工具。"""
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=3", timeout=8)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        return f"查询失败: {exc}"

# 创建带工具的 Agent
def build_agent_with_tools():
    return Agent(
        model="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        temperature=0.3,
        tools=[get_weather],
        system_prompt="你是乐于助人的助手，会在需要时调用工具。"
    )

# 使用 Agent
agent = build_agent_with_tools()
reply = agent.run("查一下北京今天的天气")  # Agent 会自动决定是否调用工具
print(reply)
```

### 3.3 使用 Assistant 组件（高级功能）

```python
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
for response in bot.run(messages):
    print(response)
```

## 4. 高级功能

### 4.1 工具调用（Function Calling）

- **注册自定义工具**：使用 `@register_tool` 装饰器或 `Tool` 类来注册自定义工具
- **多工具组合**：可以在 Agent 中注册多个工具，Agent 会根据用户请求自动选择合适的工具
- **错误处理**：确保工具函数捕获异常并返回错误信息而不是抛出异常

### 4.2 多模态处理

- **文件上传**：支持处理 PDF、图像等文件类型
- **多媒体内容**：可以处理文本和图像混合的内容

### 4.3 RAG（检索增强生成）

- 通过 `qwen-agent[rag]` 安装 RAG 功能
- 支持文档理解和知识库查询

### 4.4 代码解释器

- 通过 `qwen-agent[code_interpreter]` 启用代码执行能力
- 可以执行 Python 代码并返回结果

### 4.5 MCP（Model Context Protocol）

- 支持外部工具与模型之间的上下文协议
- 允许模型访问外部资源

### 4.6 GUI 界面

- 提供图形用户界面支持
- 使用 Gradio 实现的界面

### 4.7 内存和状态管理

- 支持长期记忆和会话状态管理
- 可以保存和恢复 Agent 的上下文

## 5. 环境配置

### 5.1 API 密钥设置

在使用 Qwen-Agent 之前，您需要设置 API 密钥：

```bash
# 设置通义千问 API 密钥
export QWEN_API_KEY="你的通义千问API密钥"

# 或者设置 DashScope API 密钥
export DASHSCOPE_API_KEY="你的DashScope API密钥"
```

### 5.2 在代码中使用环境变量

```python
import os

# 获取 API 密钥
api_key = os.getenv("QWEN_API_KEY")
if not api_key:
    print("请设置 QWEN_API_KEY 环境变量")
```

## 6. 实践练习

### 6.1 创建自定义工具

创建一个计算数学表达式的工具：

```python
import ast
import operator
from qwen_agent.tools.base import register_tool

@register_tool
def calculate(expression: str) -> str:
    """
    计算数学表达式
    """
    try:
        # 解析表达式
        node = ast.parse(expression, mode='eval')
        # 安全地评估表达式
        result = eval(compile(node, '<string>', 'eval'), 
                     {"__builtins__": {}}, 
                     {"math": __import__("math")})
        return str(result)
    except Exception as e:
        return f"计算错误: {str(e)}"
```

### 6.2 复杂任务示例

创建一个能处理多步骤任务的 Agent：

```python
from qwen_agent import Agent
import os

def build_complex_agent():
    tools = [get_weather, calculate]  # 假设已定义这两个工具
    
    return Agent(
        model="qwen-max",
        api_key=os.getenv("QWEN_API_KEY"),
        tools=tools,
        system_prompt="你是一个高级助手，可以处理复杂的多步骤任务。"
    )
```

## 7. 最佳实践

### 7.1 工具设计最佳实践

1. **明确的工具描述**：为每个工具提供清晰的描述，帮助 Agent 理解何时使用该工具
2. **参数验证**：验证传入工具的参数，确保它们符合预期
3. **错误处理**：妥善处理异常情况，返回有意义的错误信息
4. **性能考虑**：优化工具执行效率，特别是对于频繁调用的工具

### 7.2 Agent 设计最佳实践

1. **系统提示词优化**：编写清晰的系统提示词，明确 Agent 的角色和行为准则
2. **工具选择**：根据 Agent 的目标选择合适的工具集
3. **温度参数调整**：根据应用场景调整温度参数，平衡创造性和确定性

## 8. 故障排除

### 8.1 常见问题

1. **API 密钥错误**：确保正确设置了 API 密钥环境变量
2. **工具注册问题**：确保工具函数被正确装饰和注册
3. **网络连接问题**：检查网络连接和 API 服务的可用性

### 8.2 调试技巧

1. **日志记录**：启用详细的日志记录以跟踪 Agent 的决策过程
2. **逐步调试**：分别测试工具和 Agent，确保各部分正常工作
3. **错误处理**：实施适当的错误处理机制

## 9. 进一步学习资源

- Qwen-Agent 官方文档
- 通义千问模型文档
- 大语言模型应用开发指南
- 函数调用和工具使用最佳实践