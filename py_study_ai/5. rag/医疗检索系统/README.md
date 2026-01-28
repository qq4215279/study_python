# 医疗混合搜索系统

一个基于 RAG（检索增强生成）技术的医疗问答混合搜索系统，结合了向量搜索（语义搜索）和 BM25 关键词搜索。

## 功能特点

- **混合搜索**：结合向量搜索和 BM25 搜索，提供更准确的搜索结果
- **向量搜索**：使用阿里云 text-embedding-v3 模型进行语义相似度搜索
- **BM25 搜索**：基于关键词的传统信息检索方法
- **中文支持**：使用 jieba 进行中文分词
- **缓存机制**：自动缓存索引，加快后续加载速度

## 环境准备

### 1. 获取 API Key

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)
2. 开通 Model Studio / 百炼服务
3. 获取 DASHSCOPE_API_KEY

### 2. 设置环境变量

```bash
export DASHSCOPE_API_KEY='your-api-key-here'
```

或者在代码中直接传入：

```python
search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    api_key="your-api-key-here"
)
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 基本使用

```python
from medical_search_system import MedicalHybridSearchSystem

# 初始化系统（首次运行会构建索引，可能需要几分钟）
search_system = MedicalHybridSearchSystem("train_zh.json")

# 混合搜索（推荐）
results = search_system.search("头痛怎么办", top_k=5, method='hybrid')

# 向量搜索
results = search_system.search("头痛怎么办", top_k=5, method='vector')

# BM25 搜索
results = search_system.search("头痛怎么办", top_k=5, method='bm25')

# 查看结果
for result in results:
    print(f"问题: {result['instruction']}")
    print(f"回答: {result['output']}")
    print(f"分数: {result.get('hybrid_score', result.get('score', 0))}")
```

### 2. 交互式测试

运行测试脚本进行交互式搜索：

```bash
python test_search.py
```

### 3. 直接运行示例

```bash
python medical_search_system.py
```

## 搜索方法说明

### 混合搜索 (Hybrid Search)
- **原理**：结合向量搜索和 BM25 搜索的结果，通过加权融合得到最终排序
- **优点**：兼顾语义理解和关键词匹配，通常效果最好
- **权重**：默认向量搜索权重 0.7，BM25 权重 0.3（可在 `hybrid_search` 方法中调整）

### 向量搜索 (Vector Search)
- **原理**：使用 embedding 模型将文本转换为向量，通过余弦相似度计算语义相似性
- **优点**：能够理解语义，找到意思相近但用词不同的内容
- **适用场景**：查询和文档在语义上相关但用词不同

### BM25 搜索
- **原理**：基于词频和逆文档频率的传统信息检索算法
- **优点**：对精确关键词匹配效果好，速度快
- **适用场景**：查询中包含重要的专业术语或关键词

## 数据格式

系统期望的 JSON 数据格式：

```json
{"instruction": "用户问题", "input": "", "output": "医生回答"}
```

每行一个 JSON 对象。

## 配置说明

### 修改 Embedding 模型配置

在初始化时可以指定不同的配置：

```python
# 使用不同的向量维度（512/768/1024）
search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    embedding_model_name="text-embedding-v3",
    dimension=512  # 或 768, 1024
)

# 使用不同的 API 区域
# 国内区域（默认）
search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    base_url="https://dashscope.aliyuncs.com/api/v1"
)

# 国际区域
search_system = MedicalHybridSearchSystem(
    "train_zh.json",
    base_url="https://dashscope-intl.aliyuncs.com/api/v1"
)
```

### 调整混合搜索权重

```python
results = search_system.hybrid_search(
    query="头痛怎么办",
    top_k=5,
    vector_weight=0.8,  # 增加向量搜索权重
    bm25_weight=0.2    # 减少 BM25 权重
)
```

## 性能优化

- **缓存机制**：首次运行会构建索引并保存到 `./cache/` 目录，后续运行会直接加载缓存
- **批量处理**：向量生成使用批量处理，提高效率
- **索引复用**：索引构建后可以重复使用，无需重新计算

## 文件结构

```
医疗检索系统/
├── train_zh.json              # 医疗问答数据
├── medical_search_system.py   # 主程序文件
├── test_search.py             # 交互式测试脚本
├── requirements.txt           # 依赖包列表
├── README.md                  # 说明文档
└── cache/                     # 缓存目录（自动生成）
    ├── embeddings.pkl         # 向量索引缓存
    └── bm25.pkl               # BM25 索引缓存
```

## API 使用说明

### 免费额度

- 新用户通常有约 50 万 tokens 的免费额度
- 免费额度有效期通常为 90-180 天（根据地区不同）
- 详情请查看 [DashScope 计费说明](https://help.aliyun.com/zh/model-studio/billing-for-text-embedding)

### API 限制

- **批量大小**：每批最多 10 条文本（系统会自动分批处理）
- **文本长度**：单条文本最大 8192 tokens，超过会被截断
- **请求频率**：注意 API 调用频率限制

### 区域选择

- **国内区域**（默认）：`https://dashscope.aliyuncs.com/api/v1`
- **国际区域**：`https://dashscope-intl.aliyuncs.com/api/v1`

根据你的账号区域选择合适的 base_url。

## 注意事项

1. **API Key 配置**：必须设置 DASHSCOPE_API_KEY 环境变量或通过参数传入
2. **API 调用费用**：注意 API 调用费用，建议先使用免费额度测试
3. **缓存机制**：首次运行需要调用 API 构建索引，可能需要一些时间
4. **缓存文件**：确保有足够的磁盘空间存储缓存文件
5. **更新数据**：如果数据文件更新，需要删除对应的缓存文件重新构建索引
6. **网络连接**：需要能够访问阿里云 DashScope API
7. **向量维度**：支持 512/768/1024 三种维度，维度越大精度越高但存储空间也越大

## 扩展建议

- 添加更多搜索方法（如 TF-IDF、Elasticsearch 等）
- 实现搜索结果的重排序（reranking）
- 添加查询扩展功能
- 支持多轮对话上下文
- 集成大语言模型进行答案生成
