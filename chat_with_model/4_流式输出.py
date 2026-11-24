import os
from openai import OpenAI

# 1.创建调用接口的客户端
client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

completion = client.chat.completions.create(
    model="deepseek-v4.1-flash",
    messages=[{'role':'assistant','content':'You are a helpful assistant'},
                {'role': 'user', 'content': '你是谁'}],
    stream=True,
    stream_options={"include_usage":True}
)
for chunk in completion:
    # print(chunk.model_dump_json())
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            content = content.replace("\n", " ")
            print(content,
                  end = "", #换行符改为""
                  flush = True #刷新缓冲区
                  )
    elif hasattr(chunk,'usage') and chunk.usage:
        print(f"\n\nToken的使用情况：{chunk.usage}")