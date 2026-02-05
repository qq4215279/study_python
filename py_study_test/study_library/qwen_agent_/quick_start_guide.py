#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen-Agent 快速入门指南

本文件提供 Qwen-Agent 的快速上手教程
"""

import os


def quick_start():
    """
    快速开始指南
    """
    print("🚀 Qwen-Agent 快速入门指南")
    print("=" * 50)
    
    print("\n📋 第一步: 环境准备")
    print("-" * 30)
    steps = [
        "1. 确保 Python 3.8+ 已安装",
        "2. (可选) 创建虚拟环境",
        "3. 安装 qwen-agent"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    print("\n🔧 安装命令:")
    print("pip install -U \"qwen-agent[gui,rag,code_interpreter,mcp]\"")
    
    print("\n🔑 第二步: 获取 API Key")
    print("-" * 30)
    print("访问阿里云 DashScope 控制台申请 API Key")
    print("网址: https://dashscope.console.aliyun.com/")
    
    print("\n⚙️ 第三步: 配置环境变量")
    print("-" * 30)
    print("# Linux/Mac:")
    print("export DASHSCOPE_API_KEY='your_api_key_here'")
    print("\n# Windows:")
    print("set DASHSCOPE_API_KEY=your_api_key_here")
    print("\n# 或者在 Python 代码中直接设置:")
    print("os.environ['DASHSCOPE_API_KEY'] = 'your_api_key_here'")


def basic_usage():
    """
    基础使用方法
    """
    print("\n💡 基础使用方法")
    print("=" * 50)
    
    print("\n1. 最简单的聊天机器人:")
    print("-" * 25)
    simple_code = '''
from qwen_agent.agents import Assistant

# 基础配置
llm_cfg = {
    'model': 'qwen-turbo-latest',
    'model_type': 'qwen_dashscope'
}

# 创建助手
bot = Assistant(llm=llm_cfg)

# 开始对话
messages = [{'role': 'user', 'content': '你好！'}]
for response in bot.run(messages):
    print(response)
'''
    print(simple_code)
    
    print("\n2. 带工具的智能助手:")
    print("-" * 25)
    tool_code = '''
from qwen_agent.agents import Assistant

# 配置助手
llm_cfg = {
    'model': 'qwen-max-latest',
    'model_type': 'qwen_dashscope'
}

# 创建带工具的助手
bot = Assistant(
    llm=llm_cfg,
    function_list=['code_interpreter'],  # 启用代码解释器
    system_message='你是一个编程助手，可以帮助写代码和解决问题'
)

# 使用示例
messages = [{'role': 'user', 'content': '帮我写一个Python函数计算斐波那契数列'}]
for response in bot.run(messages):
    print(response)
'''
    print(tool_code)


def common_patterns():
    """
    常用模式
    """
    print("\n🎯 常用模式")
    print("=" * 50)
    
    patterns = [
        {
            "模式": "文档问答",
            "代码示例": '''
bot = Assistant(
    llm=llm_cfg,
    files=['document.pdf'],
    system_message='基于提供的文档回答问题'
)
''',
            "适用场景": "知识库问答、文档理解"
        },
        {
            "模式": "数据分析",
            "代码示例": '''
bot = Assistant(
    llm=llm_cfg,
    function_list=['code_interpreter'],
    system_message='你是一个数据分析师，可以处理CSV数据'
)
''',
            "适用场景": "数据分析、统计计算"
        },
        {
            "模式": "创意生成",
            "代码示例": '''
bot = Assistant(
    llm=llm_cfg,
    system_message='你是一个创意写作助手，帮助生成各种文本内容'
)
''',
            "适用场景": "内容创作、文案写作"
        }
    ]
    
    for i, pattern in enumerate(patterns, 1):
        print(f"\n{i}. {pattern['模式']}:")
        print(f"   适用场景: {pattern['适用场景']}")
        print("   代码示例:")
        print(pattern['代码示例'])


def troubleshooting():
    """
    故障排除
    """
    print("\n🔧 常见问题解决")
    print("=" * 50)
    
    issues = [
        {
            "问题": "ImportError: No module named 'qwen_agent'",
            "解决方法": "运行: pip install qwen-agent"
        },
        {
            "问题": "API key validation failed",
            "解决方法": "检查 DASHSCOPE_API_KEY 环境变量是否正确设置"
        },
        {
            "问题": "Connection refused",
            "解决方法": "检查网络连接和模型服务地址是否正确"
        },
        {
            "问题": "ModuleNotFoundError: No module named 'xxx'",
            "解决方法": "安装缺失的依赖包，如 pip install xxx"
        }
    ]
    
    for issue in issues:
        print(f"\n❌ {issue['问题']}")
        print(f"✅ 解决方法: {issue['解决方法']}")


def next_steps():
    """
    下一步学习
    """
    print("\n📚 进阶学习路径")
    print("=" * 50)
    
    learning_path = [
        "1. 深入学习工具开发 - 创建自定义工具",
        "2. 掌握 RAG 技术 - 构建知识问答系统",
        "3. 学习 GUI 开发 - 创建 Web 界面应用",
        "4. 了解 MCP 协议 - 扩展模型能力",
        "5. 实践项目开发 - 构建完整的 AI 应用"
    ]
    
    for step in learning_path:
        print(f"  {step}")
    
    print("\n🔗 有用资源:")
    print("• 官方文档: https://github.com/QwenLM/Qwen-Agent")
    print("• 示例代码: examples/ 目录")
    print("• 社区讨论: GitHub Issues")


def main():
    """
    主函数
    """
    # 快速开始
    quick_start()
    
    # 基础使用
    basic_usage()
    
    # 常用模式
    common_patterns()
    
    # 故障排除
    troubleshooting()
    
    # 下一步
    next_steps()
    
    print("\n" + "=" * 50)
    print("🎉 恭喜！您已经掌握了 Qwen-Agent 的基础知识")
    print("现在可以开始构建自己的 AI 应用了！")
    print("=" * 50)


if __name__ == "__main__":
    main()