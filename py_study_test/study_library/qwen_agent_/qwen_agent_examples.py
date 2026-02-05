#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen-Agent 实际运行示例

这个文件包含了可以直接运行的 Qwen-Agent 示例代码
"""

import os
import json
from typing import List, Dict, Any
import pprint


def simple_chat_example():
    """
    简单聊天示例 - 最基础的使用方式
    """
    print("=== 简单聊天示例 ===\n")
    
    try:
        from qwen_agent.agents import Assistant
        
        # 基础配置
        llm_cfg = {
            'model': 'qwen-turbo-latest',  # 使用较小的模型以节省资源
            'model_type': 'qwen_dashscope',
            # 注意：实际使用时需要设置真实的API Key
            # 'api_key': 'your_actual_api_key_here'
        }
        
        # 创建助手
        bot = Assistant(llm=llm_cfg)
        
        # 简单对话
        messages = [
            {'role': 'user', 'content': '你好！你能帮我做什么？'}
        ]
        
        print("用户:", messages[0]['content'])
        print("助手:", end=" ")
        
        # 运行对话
        for response in bot.run(messages):
            if isinstance(response, list):
                for msg in response:
                    if msg['role'] == 'assistant':
                        print(msg['content'])
            elif isinstance(response, dict) and response['role'] == 'assistant':
                print(response['content'])
                
    except ImportError:
        print("❌ 未安装 qwen-agent，请先运行: pip install qwen-agent")
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("💡 请确保已正确配置 API Key")


def custom_tool_example():
    """
    自定义工具示例
    """
    print("\n=== 自定义工具示例 ===\n")
    
    try:
        from qwen_agent.agents import Assistant
        from qwen_agent.tools.base import BaseTool, register_tool
        import json5
        
        # 注册自定义计算器工具
        @register_tool('calculator')
        class Calculator(BaseTool):
            description = '执行基本数学计算'
            parameters = [
                {
                    'name': 'expression',
                    'type': 'string',
                    'description': '数学表达式，如 "2+3*4"',
                    'required': True
                }
            ]
            
            def call(self, params: str, **kwargs) -> str:
                try:
                    expr = json5.loads(params)['expression']
                    # 安全的数学计算 (仅用于示例，生产环境建议使用专门的数学库)
                    result = eval(expr, {"__builtins__": {}}, {})
                    return f"计算结果: {expr} = {result}"
                except Exception as e:
                    return f"计算错误: {str(e)}"
        
        # 配置助手
        llm_cfg = {
            'model': 'qwen-turbo-latest',
            'model_type': 'qwen_dashscope',
        }
        
        bot = Assistant(
            llm=llm_cfg,
            function_list=['calculator'],
            system_message='你是一个数学助手，可以使用计算器工具帮助用户解决数学问题。'
        )
        
        # 测试对话
        test_queries = [
            "计算 15 + 25 * 2",
            "求 100 除以 4 的结果"
        ]
        
        for query in test_queries:
            print(f"用户: {query}")
            messages = [{'role': 'user', 'content': query}]
            
            print("助手: ", end="")
            for response in bot.run(messages):
                if isinstance(response, list):
                    for msg in response:
                        if msg['role'] == 'assistant':
                            print(msg['content'])
                elif isinstance(response, dict):
                    if response['role'] == 'assistant':
                        print(response['content'])
            print()
            
    except ImportError:
        print("❌ 未安装 qwen-agent，请先运行: pip install qwen-agent")
    except Exception as e:
        print(f"❌ 运行出错: {e}")


def environment_setup_example():
    """
    环境配置示例
    """
    print("=== 环境配置示例 ===\n")
    
    # 展示不同的配置选项
    configs = {
        "DashScope 配置": {
            'model': 'qwen-max-latest',
            'model_type': 'qwen_dashscope',
            'api_key': 'YOUR_DASHSCOPE_API_KEY',
            'generate_cfg': {
                'temperature': 0.7,
                'top_p': 0.8,
                'max_tokens': 2048
            }
        },
        
        "本地模型服务配置": {
            'model': 'Qwen3-7B-Instruct',
            'model_server': 'http://localhost:8000/v1',
            'api_key': 'EMPTY',
            'generate_cfg': {
                'temperature': 0.7,
                'top_p': 0.9
            }
        },
        
        "最小化配置": {
            'model': 'qwen-turbo-latest',
            'model_type': 'qwen_dashscope'
        }
    }
    
    for config_name, config in configs.items():
        print(f"🔧 {config_name}:")
        pprint.pprint(config, indent=2)
        print()


def practical_use_cases():
    """
    实际应用场景展示
    """
    print("=== 实际应用场景 ===\n")
    
    use_cases = [
        {
            "场景": "文档问答助手",
            "描述": "读取PDF文档并回答相关问题",
            "核心组件": ["RAG", "文件读取", "Assistant"],
            "适用领域": "知识管理、文档理解"
        },
        {
            "场景": "数据分析助手",
            "描述": "执行数据分析和可视化任务",
            "核心组件": ["代码解释器", "Assistant"],
            "适用领域": "数据分析、商业智能"
        },
        {
            "场景": "创意设计助手",
            "描述": "生成图片、设计方案等创意内容",
            "核心组件": ["自定义工具", "Assistant"],
            "适用领域": "设计、创意产业"
        },
        {
            "场景": "编程助手",
            "描述": "代码编写、调试和优化",
            "核心组件": ["代码解释器", "函数调用"],
            "适用领域": "软件开发、教育"
        }
    ]
    
    for i, case in enumerate(use_cases, 1):
        print(f"🎯 场景 {i}: {case['场景']}")
        print(f"   描述: {case['描述']}")
        print(f"   核心组件: {', '.join(case['核心组件'])}")
        print(f"   适用领域: {case['适用领域']}")
        print()


def error_handling_example():
    """
    错误处理示例
    """
    print("=== 错误处理示例 ===\n")
    
    error_examples = [
        {
            "错误类型": "API Key 缺失",
            "可能原因": "未设置 DASHSCOPE_API_KEY 环境变量或未在配置中指定",
            "解决方案": "设置环境变量或在 llm_cfg 中添加 api_key"
        },
        {
            "错误类型": "网络连接问题",
            "可能原因": "无法连接到模型服务",
            "解决方案": "检查网络连接，确认模型服务地址正确"
        },
        {
            "错误类型": "模型不存在",
            "可能原因": "指定的模型名称不正确",
            "解决方案": "检查模型名称，使用正确的模型标识符"
        },
        {
            "错误类型": "依赖缺失",
            "可能原因": "缺少必要的依赖包",
            "解决方案": "安装相应的可选依赖，如 [rag], [code_interpreter] 等"
        }
    ]
    
    for error in error_examples:
        print(f"❌ {error['错误类型']}")
        print(f"   原因: {error['可能原因']}")
        print(f"   解决: {error['解决方案']}")
        print()


def main():
    """
    主函数 - 运行所有示例
    """
    print("🚀 Qwen-Agent 实际运行示例\n")
    print("注意: 这些示例需要先安装 qwen-agent 并配置 API Key 才能正常运行\n")
    
    # 环境配置示例
    environment_setup_example()
    
    # 实际应用场景
    practical_use_cases()
    
    # 错误处理示例
    error_handling_example()
    
    # 如果已安装 qwen-agent，则运行实际示例
    try:
        import qwen_agent
        print("✅ 检测到 qwen-agent 已安装")
        print("💡 请取消注释下方代码并配置 API Key 来运行实际示例\n")
        
        # simple_chat_example()  # 取消注释来运行
        # custom_tool_example()  # 取消注释来运行
        
    except ImportError:
        print("⚠️  qwen-agent 未安装")
        print("请运行以下命令安装:")
        print("pip install qwen-agent")
        print("或者完整安装:")
        print("pip install -U \"qwen-agent[gui,rag,code_interpreter,mcp]\"")


if __name__ == "__main__":
    main()