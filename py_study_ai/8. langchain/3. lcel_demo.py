"""
 RunnableLambda + RunnableParallel + RunnablePassthrough 的使用
"""

from operator import itemgetter
import langchain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_core.runnables import chain
from models import get_lc_model_client

# 开启该参数，会输出调试信息
langchain.debug = True
# 获得访问大模型客户端
client = get_lc_model_client()


# 1. RunnableLambda
# 定义提示模版
chat_template = ChatPromptTemplate.from_template(" {a} + {b}是多少？")


# 业务函数1：获得字符串的长度
def length_function(text):
    return len(text)


# 业务函数2：将两个字符串长度的数量相乘
def _multiple_length_function(text1, text2):
    return len(text1) * len(text2)


@chain
def multiple_length_function(_dict):
    return _multiple_length_function(_dict["text1"], _dict["text2"])


# 自己的业务函数，从数据库、文件中获得数据
@chain
def test():
    pass


chain1 = chat_template | client
# 使用RunnableLambda将函数转换为与LCEL兼容的组件

chain2 = (
        {
            "a": itemgetter("foo") | RunnableLambda(length_function),
            "b": {"text1": itemgetter("foo"), "text2": itemgetter("bar")} | multiple_length_function
        }
        | chain1
)

print(chain2.invoke({"foo": "abc", "bar": "abcd"}))

print("==========>")


# In[1]:


# 2. RunnableParallel 的使用

def add_one(x: int) -> int:
    return x + 1


def mul_two(x: int) -> int:
    return x * 2


def mul_three(x: int) -> int:
    return x * 3


def mul_four(x: dict) -> int:
    return x['mul_three'] * 4


runnable_1 = RunnableLambda(add_one)
runnable_2 = RunnableLambda(mul_two)
runnable_3 = RunnableLambda(mul_three)
runnable_4 = RunnableLambda(mul_four)

chain_seq = runnable_1 | runnable_2 | runnable_3
print("chain_seq: ", chain_seq.invoke(1))

# 比如说，RAG，1、数据库；2、互联网；3...
chain2 = runnable_1 | RunnableParallel(
    mul_two=runnable_2,
    mul_three=runnable_3) | runnable_4

print(chain2.invoke(1))


# In[2]

# 3. RunnablePassthrough 的使用
# RunnablePassthrough的两种用法都将在我们后面的课程中看到
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# RunnablePassthrough原样进行数据传递
runnable = RunnableParallel(
    passed=RunnablePassthrough(),
    modified=lambda x: x["num"] + 1,
)
print(runnable.invoke({"num": 1}))

# RunnablePassthrough对数据增强后传递
runnable = RunnableParallel(
    passed=RunnablePassthrough().assign(query=lambda x: x["num"] + 2),
    modified=lambda x: x["num"] + 1,
)
print(runnable.invoke({"num": 1}))
