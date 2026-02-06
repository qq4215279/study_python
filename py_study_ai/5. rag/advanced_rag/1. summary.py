# 摘要索引优化
from langchain.storage import InMemoryByteStore
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.retrievers import MultiVectorRetriever
import uuid
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableMap

from models import get_lc_a_t_mix_clients

# 获得访问大模型和嵌入模型客户端
client, embeddings_model = get_lc_a_t_mix_clients()
# 初始化文档加载器
loader = TextLoader("./deepseek百度百科.txt", encoding="utf-8")
# 加载文档
docs = loader.load()
# 初始化递归文本分割器（设置块大小和重叠）
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# 初始化Chroma实例（用于存储摘要向量）
vectorstore = Chroma(
    collection_name="summaries",
    embedding_function=embeddings_model
)

# 初始化内存字节存储（用于存储原始文档）
store = InMemoryByteStore()

# 初始化多向量检索器（结合向量存储和文档存储）
id_key = "doc_id"
retriever = MultiVectorRetriever(
    vectorstore=vectorstore,
    byte_store=store,
    id_key=id_key,
)
# 文档的ID编号，关联我们的的摘要和原始文档
doc_ids = [str(uuid.uuid4()) for _ in docs]

# 借助大模型，把文本做相关的摘要
chain = (
        {"doc": lambda x: x.page_content}
        | ChatPromptTemplate.from_template("总结下面的文档:\n\n{doc}")
        | client
        | StrOutputParser()
)

print("准备生成文档摘要，时间稍长，请耐心等待...")
# invoke 一次调用，stream 流式调用，batch批量调用
summaries = chain.batch(docs, {"max_concurrency": 5, })
# print(summaries)

# 大模型的答复本质上是个字符串，再重新包装为Document对象
summary_docs = [
    Document(page_content=s, metadata={id_key: doc_ids[i]}) for i, s in enumerate(summaries)
]

# 将摘要添加到向量数据库
print("准备将摘要添加到向量数据库...")
retriever.vectorstore.add_documents(summary_docs)

print("准备将原始文档存储到字节存储...")
retriever.docstore.mset(list(zip(doc_ids, docs)))

# 执行相似性搜索测试，实际工作中这里其实可以不要
query = "deepseek的企业事件"
# sub_docs = retriever.vectorstore.similarity_search(query)
# print("-------------匹配的摘要内容--------------")
# print(sub_docs[0])

# 获取第一个匹配摘要的ID
# matched_id = sub_docs[0].metadata[id_key]
#
# print("-------------对应的原始文档--------------")
# # 通过ID获取原始文档
# original_doc = retriever.docstore.mget([matched_id])
# print(original_doc)
# 执行相似性搜索测试---完成


prompt = ChatPromptTemplate.from_template("根据下面的文档回答问题:\n\n{doc}\n\n问题: {question}")
chain = RunnableMap({
    "doc": lambda x: retriever.invoke(x["question"]),
    "question": lambda x: x["question"]
}) | prompt | client | StrOutputParser()

# 生成问题回答
answer = chain.invoke({"question": query})
print("-------------回答--------------")
print(answer)

# retriever.invoke将"对摘要进行检索，但是通过关联ID获得原始文档，最终返回原始文档"的过程全部都包含完成了
retrieved_docs = retriever.invoke(query)
print("-------------检索到的文档--------------")
print(retrieved_docs)
