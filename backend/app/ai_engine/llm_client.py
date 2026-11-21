# app/ai_engine/llm_client.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 初始化 DeepSeek 客户端
# DeepSeek 兼容 OpenAI SDK，只需修改 base_url
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com"
)


def call_deepseek(prompt: str) -> str:
    """
    调用 DeepSeek 模型，返回文本结果
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # 使用 deepseek-chat 模型
            messages=[
                {"role": "system", "content": "你是一个只输出纯 JSON 格式的智能助手。"},
                {"role": "user", "content": prompt},
            ],
            # 强制要求返回 JSON 格式（DeepSeek 支持此参数）
            response_format={"type": "json_object"},
            temperature=0.1,  # 调低温度，让输出更稳定、严谨
            max_tokens=500,
        )
        # 返回大模型的文本回复
        return response.choices[0].message.content
    except Exception as e:
        print(f"调用 DeepSeek API 失败: {e}")
        return ""
