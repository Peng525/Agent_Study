import os
from openai import OpenAI


class MultiTurnChat:
    def __init__(self, base_url:str, model:str, system_prompt:str = None):
        self.client = OpenAI(base_url = base_url)
        self.model = model
        self.system_prompt = system_prompt
        self.chat_history = []
        if system_prompt is not None:
            self.chat_history.append({"role":"system","content":system_prompt})

    def add_user_message(self,content:str)-> None:
        self.chat_history.append({"role":"user","content":content})

    def add_assistant_message(self, content: str)-> None:
        self.chat_history.append({"role": "assistant", "content": content})

    def send(self, user_message: str):
        self.add_user_message(user_message)
        stream = self.client.chat.completions.create(
            model = self.model,
            messages = self.chat_history,
            stream = True,
            # stream_options = {"include_usage": True}
        )

        full_reply = ""
        for chunk in stream:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                full_reply += content
                yield content # 逐块返回给调用方
        # elif hasattr(chunk, 'usage') and chunk.usage:
        #     print(f"\n\nToken的使用情况：{chunk.usage}")
        self.add_assistant_message(full_reply)
        #return full_reply  这里用了流式输出如果返回full_reply 那还是一次性返回所以要在循环中写个 yield

if "__main__" == __name__:
    BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    MODEL = "deepseek-v4.1-flash"
    SYSTEM_PROMPT = "你是一个和蔼可亲并且能用通俗语言回答用户问题的助手"
    chat = MultiTurnChat(
        base_url = BASE_URL,
        model = MODEL,
        system_prompt = SYSTEM_PROMPT
    )

    print("------------------------------------------------")
    print("多轮对话已开启，请输入内容后按回车发送。\n 输入 'exit' 或 'quit' 退出程序\n")
    while True:
        query = input("用户：")
        if query in ["exit","quit"]:
            print("程序退出！ 拜拜~")
            break
        if not query.strip():
            continue
        print("AI回复： ",end = "", flush = True)
        for chunk in chat.send(query):
            print(chunk, end = "", flush = True)
        print()