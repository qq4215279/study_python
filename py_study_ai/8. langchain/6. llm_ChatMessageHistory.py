# 消息历史组件ChatMessageHistory的使用

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from models import get_lc_model_client

chat_template = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template("你是人工智能助手"),
        # 历史消息的存放地
        MessagesPlaceholder(variable_name="messages")
        # ('placeholder',"{messages}")
    ]
)

client = get_lc_model_client()

parser = StrOutputParser()
chain = chat_template | client | parser

chat_history = ChatMessageHistory()
chat_history.add_user_message('你好，我是云帆')
response = chain.invoke({'messages': chat_history.messages})
print(response)
# 把大模型响应加入历史消息
chat_history.add_ai_message(response)
print(chat_history.messages)
chat_history.add_user_message('你好，我是谁？')
print(chain.invoke({'messages': chat_history.messages}))
