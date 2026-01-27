# 自动会话历史管理组件 RunnableWithMessageHistory
# 以及如何流式处理大模型的应答
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from models import get_lc_model_client

client = get_lc_model_client()

# 定义提示模版
prompt_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是一个聊天助手，用{language}回答所有的问题"),
        # 表示需要把以前的聊天记录作为对话内容的一部分发给大模型
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)

parser = StrOutputParser()
# 以链的形式
chain = prompt_template | client | parser

# 有一个东西，保存所有用户的所有聊天记录
store = {}

# 根据每个用户自己的session_id，去获取这个用户的聊天记录
'''这里我们是将用户的会话历史保存在本机内存中，在实际业务中一般会保存到Redis缓存,
代码一般如下所示，注意代码未经测试，只做示范：
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
def get_redis_history(session_id: str) -> BaseChatMessageHistory:
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)'''


def get_session(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


chatbot_with_his = RunnableWithMessageHistory(
    chain,
    get_session,
    input_messages_key="input",
    history_messages_key="history"
)

# 从业务角度来说，每个的Session_id遵循某种算法
config_chn = {'configurable': {'session_id': "yunfang_chinese"}}
config_eng = {'configurable': {'session_id': "yunfang_english"}}

resp = chatbot_with_his.invoke(
    {
        "input": [HumanMessage(content="你好，我是云帆。")],
        "language": "中文"
    },
    config=config_chn
)
print(resp)

resp = chatbot_with_his.invoke(
    {
        "input": [HumanMessage(content="你好，我是云帆。")],
        "language": "英文"
    },
    config=config_eng
)
print(resp)

resp = chatbot_with_his.invoke(
    {
        "input": [HumanMessage(content="请问我的名字是什么？")],
        "language": "中文"
    },
    config=config_chn
)

print(resp)

resp = chatbot_with_his.invoke(
    {
        "input": [HumanMessage(content="请问我的名字是什么？")],
        "language": "英文"
    },
    config=config_eng
)
print(resp)

# 流式处理
for respon in chatbot_with_his.stream(
        {
            "input": [HumanMessage(content="请给我说5个有趣的笑话")],
            "language": "中文"
        },
        config=config_chn
):
    print(respon, end="-")
