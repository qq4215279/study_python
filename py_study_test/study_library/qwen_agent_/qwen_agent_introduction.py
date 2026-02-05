#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen-Agent 核心 API 详细介绍及使用示例

Qwen-Agent 是基于通义千问大模型构建的智能体框架，提供了丰富的功能组件，
包括函数调用、MCP、代码解释器、RAG、浏览器扩展等能力。
"""

import os
import json
from typing import List, Dict, Any, Optional
import pprint


def introduction():
    """
    Qwen-Agent 核心概念介绍
    """
    print("=" * 60)
    print("Qwen-Agent 核心 API 介绍")
    print("=" * 60)
    
    print("\n🎯 核心特性:")
    features = [
        "🔧 函数调用 (Function Calling) - 支持工具使用和API调用",
        "📚 RAG (Retrieval-Augmented Generation) - 增强检索生成能力",
        "💻 代码解释器 (Code Interpreter) - 安全执行Python代码",
        "🌐 浏览器助手 (Browser Assistant) - 网页交互能力",
        "🔌 MCP (Model Context Protocol) - 标准化上下文协议",
        "🎨 自定义工具 - 支持注册自定义工具函数",
        "📱 GUI界面 - 基于Gradio的Web界面支持"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\n🏗️ 核心架构组件:")
    components = [
        "BaseChatModel - 基础聊天模型类",
        "BaseTool - 基础工具类",
        "Agent - 智能体基类",
        "Assistant - 助手智能体实现",
        "FnCallAgent - 函数调用智能体",
        "ReActChat - ReAct模式聊天代理"
    ]
    
    for component in components:
        print(f"  • {component}")


def core_apis_overview():
    """
    核心 API 概览
    """
    print("\n" + "=" * 60)
    print("核心 API 概览")
    print("=" * 60)
    
    apis = {
        "模型配置 (LLM Configuration)": [
            "model: 指定使用的模型名称",
            "model_type: 模型类型 (qwen_dashscope, openai_api等)",
            "api_key: API密钥",
            "model_server: 模型服务地址",
            "generate_cfg: 生成参数配置"
        ],
        
        "工具系统 (Tool System)": [
            "BaseTool: 工具基类",
            "@register_tool: 工具注册装饰器",
            "description: 工具功能描述",
            "parameters: 工具参数定义",
            "call(): 工具执行方法"
        ],
        
        "智能体 (Agent)": [
            "Assistant: 多功能助手智能体",
            "FnCallAgent: 函数调用专用智能体",
            "ReActChat: ReAct模式聊天代理",
            "system_message: 系统指令",
            "function_list: 可用工具列表",
            "files: 可读取的文件列表"
        ],
        
        "对话管理 (Conversation Management)": [
            "run(): 运行对话",
            "messages: 对话历史记录",
            "streaming: 流式输出支持"
        ],
        
        "GUI界面 (GUI Interface)": [
            "WebUI: Web界面类",
            "run(): 启动Web服务"
        ]
    }
    
    for category, items in apis.items():
        print(f"\n📌 {category}:")
        for item in items:
            print(f"  • {item}")


class QwenAgentExample:
    """Qwen-Agent 使用示例类"""
    
    def __init__(self):
        """初始化示例"""
        self.setup_environment()
    
    def setup_environment(self):
        """环境设置示例"""
        print("\n🔧 环境配置示例:")
        
        # DashScope API 配置
        dashscope_config = {
            'model': 'qwen-max-latest',
            'model_type': 'qwen_dashscope',
            'api_key': 'YOUR_DASHSCOPE_API_KEY',  # 实际使用时替换为真实API Key
            'generate_cfg': {
                'temperature': 0.7,
                'top_p': 0.8,
                'max_tokens': 2048
            }
        }
        
        print("DashScope 配置:")
        pprint.pprint(dashscope_config, indent=2)
        
        # 本地模型服务配置
        local_config = {
            'model': 'Qwen3-7B-Instruct',
            'model_server': 'http://localhost:8000/v1',
            'api_key': 'EMPTY',
            'generate_cfg': {
                'temperature': 0.7,
                'top_p': 0.9
            }
        }
        
        print("\n本地模型服务配置:")
        pprint.pprint(local_config, indent=2)
    
    def basic_chat_example(self):
        """基础聊天示例"""
        print("\n💬 基础聊天示例:")
        
        code_example = '''
# 基础聊天示例
from qwen_agent.agents import Assistant

# 配置模型
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope',
    'generate_cfg': {'temperature': 0.7}
}

# 创建助手
bot = Assistant(llm=llm_cfg)

# 进行对话
messages = [{'role': 'user', 'content': '你好，介绍一下你自己'}]
for response in bot.run(messages):
    print(response)
'''
        print(code_example)
    
    def tool_usage_example(self):
        """工具使用示例"""
        print("\n🛠️ 自定义工具示例:")
        
        code_example = '''
from qwen_agent.tools.base import BaseTool, register_tool
import json5
import requests

# 注册自定义工具
@register_tool('weather_query')
class WeatherQuery(BaseTool):
    description = '查询指定城市的天气信息'
    parameters = [{
        'name': 'city',
        'type': 'string',
        'description': '城市名称',
        'required': True
    }]
    
    def call(self, params: str, **kwargs) -> str:
        city = json5.loads(params)['city']
        # 这里可以调用真实的天气API
        return f"{city}的天气很好，温度适宜。"

# 使用工具的助手
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope'
}

bot = Assistant(
    llm=llm_cfg,
    function_list=['weather_query'],
    system_message='你是一个有用的助手，可以根据需要调用天气查询工具。'
)

# 调用示例
messages = [{'role': 'user', 'content': '北京今天天气怎么样？'}]
for response in bot.run(messages):
    print(response)
'''
        print(code_example)
    
    def rag_example(self):
        """RAG 示例"""
        print("\n📚 RAG (检索增强生成) 示例:")
        
        code_example = '''
from qwen_agent.agents import Assistant

# RAG 配置
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope'
}

# 创建带文件读取能力的助手
bot = Assistant(
    llm=llm_cfg,
    files=['./document.pdf'],  # 指定要读取的文件
    system_message='你可以阅读并理解文档内容，根据文档回答用户问题。'
)

# 基于文档的问答
messages = [{'role': 'user', 'content': '请总结这份文档的主要内容'}]
for response in bot.run(messages):
    print(response)
'''
        print(code_example)
    
    def code_interpreter_example(self):
        """代码解释器示例"""
        print("\n💻 代码解释器示例:")
        
        code_example = '''
from qwen_agent.agents import Assistant

# 配置代码解释器
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope'
}

bot = Assistant(
    llm=llm_cfg,
    function_list=['code_interpreter'],  # 启用代码解释器
    system_message='你可以编写和执行Python代码来解决问题。'
)

# 请求代码执行
messages = [{'role': 'user', 'content': '计算1到100的和'}]
for response in bot.run(messages):
    print(response)
'''
        print(code_example)
    
    def gui_example(self):
        """GUI 界面示例"""
        print("\n🖥️ GUI 界面示例:")
        
        code_example = '''
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# 创建助手
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope'
}

bot = Assistant(
    llm=llm_cfg,
    system_message='你是一个多功能助手'
)

# 启动Web界面
WebUI(bot).run()  # 默认在 http://localhost:7860 运行
'''
        print(code_example)
    
    def advanced_example(self):
        """高级综合示例"""
        print("\n🚀 高级综合示例:")
        
        code_example = '''
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.output_beautify import typewriter_print
'''


def installation_guide():
    """安装指南"""
    print("\n" + "=" * 60)
    print("📦 安装指南")
    print("=" * 60)
    
    print("\n🐍 Python 环境要求:")
    print("  • Python 3.8+ (推荐 3.10+)")
    print("  • 内存 ≥ 8GB")
    print("  • 网络连接 (访问DashScope API)")
    
    print("\n📥 安装方式:")
    
    installation_methods = [
        "# 1. 从PyPI安装稳定版",
        "pip install -U \"qwen-agent[gui,rag,code_interpreter,mcp]\"",
        "",
        "# 2. 最小化安装",
        "pip install -U qwen-agent",
        "",
        "# 3. 从源码安装最新开发版",
        "git clone https://github.com/QwenLM/Qwen-Agent.git",
        "cd Qwen-Agent",
        "pip install -e ./\"[gui,rag,code_interpreter,mcp]\""
    ]
    
    for cmd in installation_methods:
        print(f"  {cmd}")
    
    print("\n📋 可选依赖说明:")
    dependencies = [
        "[gui]: Gradio-based GUI支持",
        "[rag]: RAG支持",
        "[code_interpreter]: 代码解释器支持",
        "[mcp]: MCP支持"
    ]
    
    for dep in dependencies:
        print(f"  • {dep}")


def best_practices():
    """最佳实践"""
    print("\n" + "=" * 60)
    print("🏆 最佳实践")
    print("=" * 60)
    
    practices = [
        "🔑 API密钥安全: 使用环境变量存储API密钥，避免硬编码",
        "⚙️ 参数调优: 根据具体场景调整temperature、top_p等参数",
        "🛡️ 安全考虑: 生产环境中谨慎使用代码解释器",
        "📝 日志记录: 启用适当的日志记录便于调试",
        "🔄 错误处理: 实现完善的异常处理机制",
        "⚡ 性能优化: 合理使用缓存和批处理",
        "📏 输入验证: 对用户输入进行适当验证和清理"
    ]
    
    for practice in practices:
        print(f"  • {practice}")


def main():
    """主函数"""
    # 显示介绍
    introduction()
    
    # 核心API概览
    core_apis_overview()
    
    # 创建示例实例
    example = QwenAgentExample()
    
    # 展示各种示例
    example.basic_chat_example()
    example.tool_usage_example()
    example.rag_example()
    example.code_interpreter_example()
    example.gui_example()
    example.advanced_example()
    
    # 安装指南
    installation_guide()
    
    # 最佳实践
    best_practices()
    
    print("\n" + "=" * 60)
    print("🎉 Qwen-Agent 核心 API 介绍完成!")
    print("更多详细信息请参考官方文档: https://github.com/QwenLM/Qwen-Agent")
    print("=" * 60)


if __name__ == "__main__":
    main()