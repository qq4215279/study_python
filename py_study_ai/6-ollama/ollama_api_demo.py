"""
Ollama API 交互示例
使用 requests 库直接与 Ollama REST API 进行交互
"""

import requests
import json


# Ollama API 基础 URL（默认运行在本地 11434 端口）
BASE_URL = "http://localhost:11434"


def list_models():
    """
    列出所有可用的模型
    """
    url = f"{BASE_URL}/api/tags"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("可用模型列表:")
        for model in data.get("models", []):
            print(f"  - {model.get('name')} (大小: {model.get('size', 'N/A')} bytes)")
        return data
    except requests.exceptions.RequestException as e:
        print(f"获取模型列表失败: {e}")
        return None


def generate_text(model: str, prompt: str, stream: bool = False):
    """
    生成文本（非流式）
    
    Args:
        model: 模型名称，如 "deepseek-r1" 或 "llama3.2"
        prompt: 提示文本
        stream: 是否使用流式响应（默认 False）
    """
    url = f"{BASE_URL}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    
    try:
        if stream:
            # 流式响应
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            print(f"\n模型 {model} 的响应（流式）:")
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        print(chunk["response"], end="", flush=True)
                    if chunk.get("done", False):
                        print("\n")
                        break
        else:
            # 非流式响应
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            print(f"\n模型 {model} 的响应:")
            print(data.get("response", ""))
            return data
    except requests.exceptions.RequestException as e:
        print(f"生成文本失败: {e}")
        return None


def chat(model: str, messages: list, stream: bool = False):
    """
    聊天对话模式
    
    Args:
        model: 模型名称
        messages: 消息列表，格式: [{"role": "user", "content": "..."}, ...]
        stream: 是否使用流式响应（默认 False）
    """
    url = f"{BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }
    
    try:
        if stream:
            # 流式响应
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            print(f"\n模型 {model} 的对话响应（流式）:")
            full_response = ""
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "message" in chunk and "content" in chunk["message"]:
                        content = chunk["message"]["content"]
                        print(content, end="", flush=True)
                        full_response += content
                    if chunk.get("done", False):
                        print("\n")
                        break
            return full_response
        else:
            # 非流式响应
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            print(f"\n模型 {model} 的对话响应:")
            message = data.get("message", {})
            print(message.get("content", ""))
            return data
    except requests.exceptions.RequestException as e:
        print(f"聊天请求失败: {e}")
        return None


def pull_model(model: str):
    """
    拉取（下载）模型
    
    Args:
        model: 模型名称
    """
    url = f"{BASE_URL}/api/pull"
    payload = {
        "name": model
    }
    
    try:
        print(f"正在拉取模型 {model}...")
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                status = chunk.get("status", "")
                if status:
                    print(status)
                if chunk.get("completed", False):
                    print(f"模型 {model} 拉取完成！")
                    break
    except requests.exceptions.RequestException as e:
        print(f"拉取模型失败: {e}")


def check_ollama_status():
    """
    检查 Ollama 服务是否运行
    """
    try:
        response = requests.get(f"{BASE_URL}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Ollama API 交互示例")
    print("=" * 60)
    
    # 检查 Ollama 服务状态
    if not check_ollama_status():
        print("错误: Ollama 服务未运行，请确保 Ollama 已启动")
        print("提示: 运行 'ollama serve' 启动服务")
        exit(1)
    
    print("\n✓ Ollama 服务运行正常\n")
    
    # 1. 列出所有可用模型
    print("1. 列出所有可用模型")
    print("-" * 60)
    list_models()
    
    # 2. 使用 generate API 生成文本（非流式）
    print("\n2. 使用 generate API 生成文本（非流式）")
    print("-" * 60)
    generate_text(
        model="deepseek-r1",
        prompt="请用一句话介绍 Python 编程语言。",
        stream=False
    )
    
    # 3. 使用 generate API 生成文本（流式）
    print("\n3. 使用 generate API 生成文本（流式）")
    print("-" * 60)
    generate_text(
        model="deepseek-r1",
        prompt="请用三句话介绍人工智能。",
        stream=True
    )
    
    # 4. 使用 chat API 进行对话（非流式）
    print("\n4. 使用 chat API 进行对话（非流式）")
    print("-" * 60)
    chat(
        model="deepseek-r1",
        messages=[
            {"role": "user", "content": "为什么天空是蓝色的？"}
        ],
        stream=False
    )
    
    # 5. 使用 chat API 进行多轮对话（流式）
    print("\n5. 使用 chat API 进行多轮对话（流式）")
    print("-" * 60)
    chat(
        model="deepseek-r1",
        messages=[
            {"role": "user", "content": "什么是机器学习？"},
            {"role": "assistant", "content": "机器学习是人工智能的一个分支..."},
            {"role": "user", "content": "它有哪些主要类型？"}
        ],
        stream=True
    )
    
    # 6. 拉取模型示例（注释掉，避免意外下载）
    # print("\n6. 拉取模型示例")
    # print("-" * 60)
    # pull_model("llama3.2")
    
    print("\n" + "=" * 60)
    print("示例演示完成！")
    print("=" * 60)
