import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document

from models import ALI_TONGYI_API_KEY_OS_VAR_NAME, ALI_TONGYI_EMBEDDING_MODEL, get_ali_model_client

# 获得访问大模型客户端
client = get_ali_model_client()

# 直接了解LangChain中的“文档”(Document)的具体内容，这里我们跳过了文档与文档加载，文档切割和文档转换过程
# 文档的模拟数据
documents = [
    Document(
        page_content="猫是柔软可爱的动物，但相对独立",
        metadata={"source": "常见动物宠物文档"},
    ),
    Document(
        page_content="狗是人类很早开始的动物伴侣，具有团队能力",
        metadata={"source": "常见动物宠物文档"},
    ),
    Document(
        page_content="金鱼是我们常常喂养的观赏动物之一，活泼灵动",
        metadata={"source": "鱼类宠物文档"},
    ),
    Document(
        page_content="鹦鹉是猛禽，但能够模仿人类的语言",
        metadata={"source": "飞禽宠物文档"},
    ),
    Document(
        page_content="兔子是小朋友比较喜欢的宠物，但是比较难喂养",
        metadata={"source": "常见动物宠物文档"},
    ),
]

# 使用阿里的嵌入模型
from langchain_community.embeddings import DashScopeEmbeddings

llm_embeddings = DashScopeEmbeddings(
    model=ALI_TONGYI_EMBEDDING_MODEL, dashscope_api_key=os.getenv(ALI_TONGYI_API_KEY_OS_VAR_NAME))
# 使用LangChain中对Chroma的包装
vector_store = Chroma.from_documents(documents=documents, embedding=llm_embeddings)

# print(vector_store.similarity_search("狸花猫"))
# #? L2 还是cosin？越相似，分数越小,所以是L2
# print(vector_store.similarity_search_with_score("狸花猫"))

# 检索器
docs_find = RunnableLambda(vector_store.similarity_search).bind(k=1)

message = """
仅使用提供的上下文回答下面的问题：
{question}
上下文：
{context}
"""
prompt_template = ChatPromptTemplate.from_messages([('human', message)])
# 定义这个链的时候，还不知道用户的问题，所以需要一个占位符
# RunnablePassthrough()允许我们将用户的问题在程序运行时动态传入
chain = {"question": RunnablePassthrough(), "context": docs_find} | prompt_template | client
resp = chain.invoke("请介绍一下猫")
print(resp)
print(resp.content)
