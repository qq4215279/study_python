
rag: 通用基础性问题  知识密集型问题   垂直领域问题

conda 环境管理项目

ai编程工具：cursor  Trea

## python 编程库
- openai 
- dashscope
- qwen_agent
- langchain 
  - langchain 
    - langchain_core 
    - langchain_community
    - langchain_openai 
    - langchain-experimental
    - langserve  服务部署
  - chromadb 数据库
  - gradio  开源web页面
  - flask Python Web框架，给可视化大屏提供数据接口
  - fastapi web框架
  - uvicorn web服务
  - pandas 数据处理库（清洗、整理分析、合并）
  - numpy 数组运算 - 矩阵运算库
  - scipy 科学计算库
  - matplotlib 图表绘制
  - Seaborn 数据可视化(热力图/分布图)
  - dotenv 环境变量
  - scikit-learn 机器学习库
  - tensorflow 深度学习库
  - pytorch 深度学习库
  - inspect 获取对象属性
  - operator 运算符
  - tesseract 用于光学字符识别 （OCR）
  - PaddleOCR 用于图像识别
  - poppler ：用于 PDF 渲染和处理
  - sklearn 机器学习库
  - jupyter  是一个基于 Web 的交互式计算平台，使用户能够创建和共享文档，这些文档包含实时代码、方程式、可视化图表和解释文字。Jupyter 在数据分析领域被广泛应用，它提供了一个直观、交互式的操作界面，使得用户能够更容易地探索数据、可视化数据以及进行数据处理和建模的实验。
    Jupyter 不仅能够对 Python 代码进行展示和格式化，还能够保存用户的历史代码和结果以及数据分析结果。这些结果可以在后期随时查看和修改，使得 Python 的学习和应用变得更加方便和高效。
    安装：pip install jupyter
    启动：jupyter notebook 或 jupyter lab
    打开浏览器，输入 http://localhost:8888 即可访问 Jupyter 主页。
  - jieba 中文分词库
  - rank_bm25  从 rank_bm25 库中导入 BM25Okapi 类，用于计算 BM25 相似度得分
  - pickle 序列化
  - hashlib 哈希算法
  - requests 网络请求库
  - seaborn  数据可视化
  - PyPDF2 PDF文本提取
  - 文档处理库: PyMuPDF (处理PDF), python-docx (处理Word), pytesseract (OCR识别图片中的文字)
  - FlagEmbedding 是一个开源的 embedding 模型工具库，由智谱 AI 开发，主要用于文本相似度计算、语义检索等任务。
  - pymysql 数据库操作
  - loguru 日志库
  - ollama

web开发: django / flask
爬虫: python  requests  scrapy  
数据分析: numpy pandas  matplotlib  pyecharts
人工智能: 机器学习，深度学习   
自动化运维: Python运维
自动化测试: selenium Python  
少儿编程: Scratch, Python

kimi 
gemini

Cython ？

Ollama 是一个开源框架，专为在本地机器上便捷部署和运行大模型而设计。


什么是大模型开发   https://blog.csdn.net/2401_84204207/article/details/146120799
我们将开发以大语言模型为功能核心、通过大语言模型的强大理解能力和生成能力、结合特殊的数据或业务逻辑来提供独特功能的应用称为大模型开发。



tavily.com


Fitten Code    PyCharm 版 Python AI 编程助手

OpenGVLab
MinerU 文档解析

jupyter lab


ai 工作流 n8n


cursor 规则
1、之前完成正确的功能，尽量不要修改。
比如当前的instruction是完善功能A的，那么只需要专注功能A，不需要修改其他功能（比如功能B）。
2、生成的注释用中文，并使用 UTF-8 编码。
3、生成的代码有时候会存在中文乱码的情况，所以你在生成中文的时候，需要检查是否有中文乱码，如果有乱码需要修正。
4、如果修改某个函数的实现，先理解之前函数实现的逻辑。然后在原来的基础上，再进行修改（保留之前的函数逻辑，不要移除）