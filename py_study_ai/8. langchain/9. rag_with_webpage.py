import os
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser

from models import get_ali_embeddings, get_ali_model_client

# 获得访问大模型客户端
client = get_ali_model_client()

# 获得一个嵌入模型的实例
llm_embeddings = get_ali_embeddings()

# 获得文档，文档内容来自网页https://www.news.cn/fortune/20250212/895ac6738b7b477db8d7f36c315aae22/c.html
# 文档加载器
loader = WebBaseLoader(
    web_path=["https://www.news.cn/fortune/20250212/895ac6738b7b477db8d7f36c315aae22/c.html"],
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(class_=("main-left left", "title"))
    )
)
docs = loader.load()
# 文本的切割
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = splitter.split_documents(docs)
for s in documents:
    print(s, end="**\n")

# 实例化向量空间
vector_store = Chroma.from_documents(documents=documents, embedding=llm_embeddings)
# 拿到一个检索器
retriever = vector_store.as_retriever()

# 整合
system_prompt = """
您是问答任务的助理。使用以下的上下文来回答问题，
上下文：<{context}>
如果你不知道答案，不要其他渠道去获得答案，就说你不知道。
"""
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)

json_output_parser = JsonOutputParser()


# TODO
chain22 = {"question": RunnablePassthrough(), "context": retriever} | prompt_template | client | json_output_parser

# LangChain准备好了链，可以直接用
# chain1 = create_stuff_documents_chain(client,prompt_template)
# chain22 = create_retrieval_chain(retriever,chain1)

# 用大模型生成答案
resp = chain22.invoke({"input": "张成刚说了什么？"})
# 可以看到，大模型的应答中有context字段，类型是Document(metadata,page_content)的列表，answer则是大模型的回复。
print(type(resp))
print(resp)
