# 学会利用LangChain部署我们的应用成为WEB服务
from fastapi import FastAPI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langserve import add_routes

from models import get_lc_model_client

# 获得访问大模型客户端
client = get_lc_model_client()

# 解析返回结果
parser = StrOutputParser()

# 定义提示模版
prompt_template = ChatPromptTemplate.from_messages(
    [
        # 改为 ('system','请将以下的内容翻译成{language}') 也可以
        SystemMessagePromptTemplate.from_template("请将以下的内容翻译成{language}"),
        # 改为 HumanMessagePromptTemplate.from_template("{text}") 也可以
        ('human', '{text}')
    ]
)

# 以链的形式调用
chain = prompt_template | client | parser

# 部署为服务
app = FastAPI(title="基于LangChain的大模型应用", version="V1.5", description="翻译服务")
add_routes(app, chain, path="/tslServer")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
