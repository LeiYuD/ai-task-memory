# app/services/msg_service.py

from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.task import Task
from app.ai_engine import extract_task_from_text
from datetime import datetime


def get_unprocessed_messages(db: Session, limit: int = 10):
    return db.query(Message).filter(Message.is_processed == 0).limit(limit).all()


def process_message_with_ai(db: Session, message: Message, user_threshold: float = 0.7):
    """
    处理单封邮件：调用 AI -> 解析结果 -> 存为候选任务
    """
    # 1. 拼接带时间的邮件上下文
    time_str = (
        message.msg_time.strftime("%Y-%m-%d %H:%M:%S") if message.msg_time else "未知"
    )
    email_context = f"邮件接收时间: {time_str}\n发件人: {message.sender_name}\n主题: {message.subject}\n正文: {message.content}"

    # 2. 调用大模型
    ai_result = extract_task_from_text(email_context)

    # 3. 如果 AI 认为包含任务，且置信度高于阈值
    if ai_result.get("has_task") and ai_result.get("confidence", 0) >= user_threshold:
        task_data = ai_result.get("task_data", {})

        # 尝试解析 AI 返回的截止时间
        deadline_str = task_data.get("deadline")
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass

        # 4. 写入 Task 表
        new_task = Task(
            user_id=message.user_id,
            source_msg_id=message.id,
            title=task_data.get("title", "未命名任务"),
            description=task_data.get("description", ""),
            deadline=deadline,
            status="CANDIDATE",
            confidence=ai_result.get("confidence", 1.0),
        )
        db.add(new_task)

    # 5. 标记消息已处理（防止重复调用 AI）
    message.is_processed = 1
    db.commit()
