#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Qwen Agent 快速入门脚本
此脚本演示了 Qwen Agent 的基本用法和功能
"""

import os
import sys
from learning_guide import run_all_examples, build_agent_with_tools, get_weather


def show_menu():
    """
    显示菜单选项
    """
    print("\n" + "="*50)
    print("Qwen Agent 快速入门")
    print("="*50)
    print("1. 运行所有示例")
    print("2. 测试工具调用（天气查询）")
    print("3. 交互式对话")
    print("4. 查看环境配置")
    print("5. 退出")
    print("-"*50)


def check_env():
    """
    检查环境配置
    """
    print("\n环境配置检查:")
    qwen_api_key = os.getenv("QWEN_API_KEY")
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    
    if qwen_api_key:
        print("✓ QWEN_API_KEY 已设置")
    else:
        print("✗ QWEN_API_KEY 未设置")
        
    if dashscope_api_key:
        print("✓ DASHSCOPE_API_KEY 已设置")
    else:
        print("✗ DASHSCOPE_API_KEY 未设置")
        
    print("\n如需设置 API 密钥，请执行以下命令:")
    print("# 设置通义千问 API 密钥")
    print("export QWEN_API_KEY=\"你的API密钥\"")
    print("# 或者设置 DashScope API 密钥")
    print("export DASHSCOPE_API_KEY=\"你的API密钥\"")


def interactive_chat():
    """
    交互式对话功能
    """
    if not os.getenv("QWEN_API_KEY"):
        print("\n错误: 未设置 QWEN_API_KEY 环境变量")
        print("请先设置 API 密钥再运行此功能")
        return
        
    print("\n启动交互式对话...")
    print("输入 'quit' 或 'exit' 退出对话")
    
    agent = build_agent_with_tools()
    
    while True:
        try:
            user_input = input("\n你: ").strip()
            if user_input.lower() in ["quit", "exit", "退出"]:
                print("再见!")
                break
                
            if not user_input:
                continue
                
            # Agent 回复
            reply_generator = agent.run(user_input)
            reply = ""
            for response in reply_generator:
                if isinstance(response, list):
                    for item in response:
                        if 'content' in item:
                            reply = item['content']
                else:
                    reply = response
                    
            print(f"智能体: {reply}")
            
        except KeyboardInterrupt:
            print("\n\n对话已退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            break


def test_weather_tool():
    """
    测试天气工具
    """
    if not os.getenv("QWEN_API_KEY"):
        print("\n错误: 未设置 QWEN_API_KEY 环境变量")
        print("请先设置 API 密钥再运行此功能")
        return
        
    print("\n测试天气工具...")
    cities = ["Beijing", "Shanghai", "Hangzhou"]
    
    for city in cities:
        print(f"\n查询 {city} 的天气:")
        result = get_weather(city)
        print(f"结果: {result}")


def main():
    """
    主函数
    """
    while True:
        show_menu()
        choice = input("请选择一个选项 (1-5): ").strip()
        
        if choice == "1":
            print("\n正在运行所有示例...")
            run_all_examples()
        elif choice == "2":
            test_weather_tool()
        elif choice == "3":
            interactive_chat()
        elif choice == "4":
            check_env()
        elif choice == "5":
            print("\n感谢使用 Qwen Agent 快速入门!")
            sys.exit(0)
        else:
            print("\n无效的选择，请重新输入")


if __name__ == "__main__":
    main()