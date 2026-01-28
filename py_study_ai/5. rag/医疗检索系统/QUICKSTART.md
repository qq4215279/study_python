# 快速开始指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

## 2. 配置 API Key

### 方法一：环境变量（推荐）

```bash
# Linux/Mac
export DASHSCOPE_API_KEY='your-api-key-here'

# Windows
set DASHSCOPE_API_KEY=your-api-key-here
```

### 方法二：代码中传入

```python
from medical_search_system import MedicalHybridSearchSystem

search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    api_key="your-api-key-here"
)
```

## 3. 运行示例

```bash
# 运行基础示例
python medical_search_system.py

# 运行详细示例
python example.py

# 运行交互式测试
python test_search.py
```

## 4. 基本使用

```python
from medical_search_system import MedicalHybridSearchSystem

# 初始化（首次运行会调用 API 构建索引）
search_system = MedicalHybridSearchSystem("train_zh.json")

# 混合搜索
results = search_system.search("头痛怎么办", top_k=5, method='hybrid')

# 查看结果
for result in results:
    print(f"问题: {result['instruction']}")
    print(f"回答: {result['output']}")
    print(f"混合分数: {result['hybrid_score']:.4f}\n")
```

## 常见问题

### Q: 如何获取 API Key？
A: 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)，开通服务后获取。

### Q: 首次运行很慢？
A: 首次运行需要调用 API 为所有数据生成向量，需要一些时间。后续会使用缓存，速度会很快。

### Q: 如何更换向量维度？
A: 在初始化时指定 `dimension` 参数：
```python
search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    dimension=512  # 或 768, 1024
)
```

### Q: 如何清除缓存重新构建索引？
A: 删除 `cache` 目录即可。
