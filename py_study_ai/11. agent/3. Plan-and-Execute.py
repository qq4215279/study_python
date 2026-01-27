from langchain_openai import ChatOpenAI
from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner
from langchain import SerpAPIWrapper
from langchain.agents import Tool
from langchain import LLMMathChain
from dotenv import load_dotenv

load_dotenv()
# 配置API密钥和基础URL
llm = ChatOpenAI(model="gpt-4o-mini")

# 创建工具
search = SerpAPIWrapper()
llm_math_chain = LLMMathChain(llm=llm, verbose=True)

# 定义工具列表
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="用于回答关于当前事件的问题"
    ),
    Tool(
        name="Calculator",
        func=llm_math_chain.run,
        description="用于计算或解决问题"
    )
]

# 加载规划器和执行器
planner = load_chat_planner(llm)

executor = load_agent_executor(llm, tools, verbose=True)

# 创建Plan and Execute代理
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)

# 运行代理解决实际问题
print(agent.invoke({"input": "在中国，100人民币能买几束玫瑰花？"}))
