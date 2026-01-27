from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from langchain.chains import LLMMathChain
from langchain.prompts import MessagesPlaceholder
from langchain_community.agent_toolkits.load_tools import load_tools
from dotenv import load_dotenv

load_dotenv()

""" AgentExecutor """
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
)

# 构建一个搜索工具
search = SerpAPIWrapper()

# 创建一个数学计算工具
llm_math_chain = LLMMathChain(
    llm=llm,
    verbose=True
)

# 定义内部工具
# tools = load_tools(["serpapi", "llm-math"], llm=llm)
# 自动以工具
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="useful for when you need to answer questions about math"
    ),
]

print(tools)

# 记忆组件
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True, # 是否打印日志
    handle_parsing_errors=True,  # 处理解析错误
    agent_kwargs={
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history"),
                                  MessagesPlaceholder(variable_name="agent_scratchpad")],
    },
    memory=memory  # 记忆组件
)

agent_chain.invoke({"input": "你好"})
agent_chain.invoke({"input": "我叫Cat，很高兴见到你"})
agent_chain.invoke({"input": "1+1等于几？"})
agent_chain.invoke({"input": "好厉害，刚才我们都聊了什么？"})
