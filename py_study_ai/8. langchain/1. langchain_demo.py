
from models import get_lc_model_client
import os
import dashscope

# 0 - langchain-openai
from langchain_openai import OpenAI, ChatOpenAI

# 1. langchain 包
# 开启设置debug
import langchain
# 开启调试模型
langchain.debug = True
# 创建代理
from langchain.agents import create_agent



# 2. langchain_core 包
#  Document模块
from langchain_core.documents import Document

# . 嵌入模块
from langchain_core.embeddings.embeddings import Embeddings

# . 消息模块
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
#
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
# . 聊天提示词模块
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
# 少样本提示模版的使用
from langchain_core.prompts.few_shot import FewShotPromptTemplate

# . 运行模块
from langchain_core.runnables import RunnableSequence, RunnableLambda, RunnableParallel, RunnablePassthrough, RunnableWithMessageHistory, RunnableConfig

# . 语言模型模块解析输出
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser, JsonOutputParser, XMLOutputParser
# from langchain_core.output_parsers import DatetimeOutputParser    where？？？

# . 向量存储模块
from langchain_core.vectorstores import  VectorStore, VectorStoreRetriever, InMemoryVectorStore

# . 工具模块
from langchain_core.tools import Tool



# 3. langchain_community 包
# . 向量嵌入模块
from langchain_community.embeddings import DashScopeEmbeddings

# . 网页文档加载器
from langchain_community.document_loaders import WebBaseLoader

# .
from langchain_community.vectorstores import Chroma

from langchain_community.agent_toolkits import SQLDatabaseToolkit

# LangChain访问MySQL数据库
from langchain_community.utilities import SQLDatabase

# . 道具sql工具
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.tools import TavilySearchResults

# 导入通义千问Tongyi模型
from langchain_community.llms import Tongyi


# 4. langchain_text_splitters 文档加载模块
from langchain_text_splitters import RecursiveCharacterTextSplitter


# 5. 向量数据库模块
from langchain_chroma import Chroma





# . 文档检索模块     where???
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain.chains.retrieval import create_retrieval_chain
# from langchain.chains.sql_database.query import create_sql_query_chain

# 获得访问大模型客户端
client = get_lc_model_client()

#原始的文字模版，其中用{}的部分是占位符，可以在运行时动态替换
template_str = "您是一位专业的程序员。\n对于信息 {text} 进行简短描述"
fact_text = "langchain"
# 方法1. 根据原始的文字模版创建LangChain中的提示模版
prompt = PromptTemplate.from_template(template_str)
print("prompt: " + prompt.format(text=fact_text))
# 方法2. PromptTemplate使用，还有第二种用法，有明显的约束，要求使用该模版时，必给变量 {text} 赋值
prompt2 = PromptTemplate(
    input_variables=["text"],
    template=template_str
)

chat_template = ChatPromptTemplate.from_messages(
    [
        # 用 SystemMessagePromptTemplate 来实现可以
        ('system',"请将以下的内容翻译成{language}"),
        HumanMessagePromptTemplate.from_template("{text}")
        #('human',"{text"),
    ]
)

# 定义结果解析器
parser = StrOutputParser()
output_parser = JsonOutputParser()

# 创建一个链，将提示模版和模型连接起来
# 使用 RunnableSequence()  等价于 通过 | 拼接
# chain = RunnableSequence(chat_template, client, parser)
chain = chat_template | client | parser
# 接收的字典类型
print(chain.invoke({'text': '你好，我是云帆', 'language': '英文'}))


# In[3]
# 从环境变量获取 dashscope 的 API Key
api_key = os.environ.get('DASHSCOPE_API_KEY')
dashscope.api_key = api_key
# 加载 Tongyi 模型
llm = Tongyi(model_name="qwen-turbo", dashscope_api_key=api_key)  # 使用通义千问qwen-turbo模型
# 新推荐用法：将 prompt 和 llm 组合成一个"可运行序列"
chain3 = prompt | llm

# 使用 invoke 方法传入输入
result3 = chain3.invoke({"product": "colorful socks"})
print("result3: ", result3)