# app/ai_engine/prompt.py


def get_task_extraction_prompt(email_context: str) -> str:
    """
    构建用于提取邮件任务的 Prompt
    """
    return f"""你是一个专业的日程与任务提取助手。请阅读以下邮件内容，判断是否包含待办事项、会议通知或重要任务。
提取规则：
1. 忽略广告、系统退信、无实际意义的寒暄。
2. 如果包含任务，请提取出：任务标题（精简）、截止时间（格式为 YYYY-MM-DD HH:MM:SS，若无则为 null）、置信度（0.0-1.0）。
3. **特别注意**：如果邮件里说“明天”、“下周五”，请结合邮件发送时间推算出具体的截止日期。
4. 如果没有任务，has_task 设为 false。

请严格按以下 JSON 格式输出，不要输出任何额外的解释文字：
{{
  "has_task": true,
  "confidence": 0.9,
  "task_data": {{
    "title": "提交项目报告",
    "description": "导师发邮件要求下周三前提交报告",
    "deadline": "2026-11-25 18:00:00"
  }}
}}

邮件内容：
\"\"\"
{email_context}
\"\"\"
"""
