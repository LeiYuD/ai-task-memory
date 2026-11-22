# app/services/task_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task
from app.schemas.task_schema import TaskUpdate
from app.ai_engine.llm_client import call_deepseek
from app.ai_engine.prompt import get_task_extraction_prompt
import json


def get_tasks_by_status(db: Session, user_id: int, status: str) -> List[Task]:
    """获取指定状态的任务列表"""
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == status)
        .order_by(Task.created_at.desc())
        .all()
    )

    # 把来源邮件的接收时间动态挂载到 task 对象上
    for task in tasks:
        if task.source_message:
            task.source_msg_time = task.source_message.msg_time

    return tasks


def update_task_status(
    db: Session, task_id: int, user_id: int, new_status: str
) -> bool:
    """更新任务状态（如：确认任务，标记完成，删除）"""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return False

    task.status = new_status
    db.commit()
    return True


def update_task_info(
    db: Session, task_id: int, user_id: int, task_in: TaskUpdate
) -> Optional[Task]:
    """人工改写任务内容（支持局部更新）"""
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def process_chat_to_task(db: Session, chat_text: str, user_id: int) -> dict:
    """处理用户与 AI 的对话，提取任务并直接入库"""
    prompt = get_task_extraction_prompt(chat_text)
    raw_response = call_deepseek(prompt)

    try:
        ai_result = json.loads(raw_response)
    except:
        return {"has_task": False, "reply": "我没太听懂，请换个说法试试？"}

    if ai_result.get("has_task"):
        task_data = ai_result.get("task_data", {})
        new_task = Task(
            user_id=user_id,
            title=task_data.get("title", "未命名任务"),
            description=task_data.get("description", chat_text),
            status="CANDIDATE",
            confidence=ai_result.get("confidence", 1.0),
        )
        db.add(new_task)
        db.commit()

        return {
            "has_task": True,
            "reply": f"✅ 收到！我已经帮你把「{new_task.title}」加进收件箱啦。",
            "task": task_data,
        }

    return {
        "has_task": False,
        "reply": "这段话里好像没有需要记录的具体任务哦，你可以试试说：'明天下午3点开会'。",
    }
