import os
from openai import OpenAI

# 1.创建调用接口的客户端
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    #OPENAI代码显示如果没有API KEY会自动去系统变量中找 OPENAI_API_KEY
    api_key= os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用接口 并存储模型的回复
completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen3.8-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁？"},
    ]
)
# 3.打印完整的回复内容
print(completion.model_dump_json())

# 只打印我们需要的大模型回复的内容
print(completion.choices[0].message.content)