# 父子文档检索优化

import os
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings.dashscope import DashScopeEmbeddings
from langchain.retrievers import ParentDocumentRetriever
from langchain_core.stores import InMemoryStore
from  langchain_openai.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap
from langchain_core.output_parsers import StrOutputParser
from models import  get_lc_a_t_mix_clients

#获得访问大模型和嵌入模型客户端
client,embeddings_model = get_lc_a_t_mix_clients()

# 加载数据
loader = TextLoader("./deepseek百度百科.txt",encoding="utf-8")
docs = loader.load()

# 查看长度
print(f"文章的长度：{len(docs[0].page_content)}")

parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1024)

child_splitter = RecursiveCharacterTextSplitter(chunk_size=256)

# 创建向量数据库对象
vectorstore = Chroma(
    collection_name="split_parents", embedding_function = embeddings_model
)
# 创建内存存储对象
store = InMemoryStore()
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": 1}
)

#添加文档集
retriever.add_documents(docs)

print(f"主文块的数量：{len(list(store.yield_keys()))}")

# 测试 - 相似性搜索
print("------------similarity_search------------------------")
sub_docs = vectorstore.similarity_search("deepseek的应用场景")
print(sub_docs[0].page_content)

print("------------get_relevant_documents------------------------")
retrieved_docs = retriever.invoke("deepseek的应用场景")
print(retrieved_docs[0].page_content)

# #创建prompt模板
# template = """请根据下面给出的上下文来回答问题:
# {context}
# 问题: {question}
# """
#
# #由模板生成prompt
# prompt = ChatPromptTemplate.from_template(template)
#
# #创建chain
# chain = RunnableMap({
#     "context": lambda x: retriever.invoke(x["question"]),
#     "question": lambda x: x["question"]
# }) | prompt | client | StrOutputParser()
#
# print("------------模型回复------------------------")
#
# response = chain.invoke({"question": "deepseek的应用场景"})
# print(response)
