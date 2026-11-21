# app/ai_engine/extractor.py

import json
from app.ai_engine.prompt import get_task_extraction_prompt
from app.ai_engine.llm_client import call_deepseek


def extract_task_from_text(email_context: str) -> dict:
    """
    从邮件文本中提取任务。
    """
    if not email_context or len(email_context.strip()) == 0:
        return {"has_task": False}

    # 1. 构建 Prompt
    prompt = get_task_extraction_prompt(email_context)

    # 2. 调用 DeepSeek
    raw_response = call_deepseek(prompt)

    if not raw_response:
        return {"has_task": False, "error": "API call failed"}

    # 3. 解析 JSON
    try:
        result = json.loads(raw_response)
        return result
    except json.JSONDecodeError:
        print(f"AI 返回的格式不是标准 JSON: {raw_response}")
        return {"has_task": False, "error": "JSON parse error"}
