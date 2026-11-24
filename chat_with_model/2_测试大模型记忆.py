import os
from openai import OpenAI

# 1.创建调用接口的客户端
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx"
    #OPENAI代码显示如果没有API KEY会自动去系统变量中找 OPENAI_API_KEY
    api_key= os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 2.调用接口 发起第一次请求 5c
completion = client.chat.completions.create(
    # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    model="qwen3.8-flash",
    messages=[
        {"role": "user", "content": "你好，我是小彭，我是一个正在学习agent的学生"}
    ]
)
# 3.打印完整的回复内容
#print(completion.model_dump_json())

# 只打印我们需要的大模型回复的内容
print("不附加上下文第一次调用：" + completion.choices[0].message.content)

# 4.再次提问
completion2 = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=[
        {"role":"user","content":"我是谁"}
    ]
)
print("------------------------------------------------------------")
print("不附加上下文第二次调用：" + completion2.choices[0].message.content)

# 附加上下文需要构造上下文列表
chat_history = []

user_message_1 = "你好，我是小彭，我是一个正在学习agent的学生"
chat_history.append({"role":"user","content":user_message_1})
completion3 = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=chat_history
)

# 将回答也加入上下文
chat_history.append({"role":"assistant","content":completion2.choices[0].message.content})
'''如果这里把role写成ai在调用接口时会报错:
   openai.BadRequestError. 错误码: 400- 'error': 'message: ai 不是"system", "assistant',"user',"tool","function"] 中任何一个, 'type': 'invalid request error'
   原因： openai 中 assistant 代表 ai 的回复
'''

print("------------------------------------------------------------")
print("附加上下文第一次调用：" + completion3.choices[0].message.content)

# 第二次调用
user_message_2 = "我是谁"
chat_history.append({"role":"user","content":user_message_2})
completion4 = client.chat.completions.create(
    model="qwen3.8-flash",
    messages=chat_history
)
print("------------------------------------------------------------")
print("附加上下文第二次调用：" + completion4.choices[0].message.content)