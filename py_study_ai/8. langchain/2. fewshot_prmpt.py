# 少样本提示模版的使用
from langchain_core.prompts import PromptTemplate
from langchain_core.prompts.few_shot import FewShotPromptTemplate
from models import get_lc_model_client

# 获得访问大模型客户端
client = get_lc_model_client()

# 创建示例的文本
examples = [
    {"sinput": "2+2", "soutput": "4", "sdescription": "加法运算"},
    {"sinput": "5-2", "soutput": "3", "sdescription": "减法运算"},
]

# 配置一个提示模板，用来一个示例格式化
examples_prompt_tmplt_txt = "算式： {sinput} 值： {soutput} 类型： {sdescription} "

# 这是一个提示模板的实例，用于设置每个示例的格式
prompt_sample = PromptTemplate.from_template(examples_prompt_tmplt_txt)

'''    
prefix="你是一个数学专家, 能够准确说出算式的类型，",
suffix="现在给你算式: {input} ， 值: {output} ，告诉我类型：",'''

prompt = FewShotPromptTemplate(
    example_prompt=prompt_sample,
    examples=examples,
    prefix="你是一个数学专家, 能够准确说出算式的类型，",
    suffix="现在给你算式: {input} ， 值: {output} ，告诉我类型：",
    input_variables=["input", "output"])

print(prompt.format(input="2*5", output="10"))
print('-' * 50)

result = client.invoke(prompt.format(input="2*5", output="10"))
print(result.content)  # 使用: 乘法运算
