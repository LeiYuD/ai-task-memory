# app/services/task_service.py

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.task import Task
from app.schemas.task_schema import TaskUpdate


def get_tasks_by_status(db: Session, user_id: int, status: str) -> List[Task]:
    """获取指定状态的任务列表"""
    return (
        db.query(Task)
        .filter(Task.user_id == user_id, Task.status == status)
        .order_by(Task.created_at.desc())
        .all()
    )


def update_task_status(
    db: Session, task_id: int, user_id: int, new_status: str
) -> bool:
    """更新任务状态（如：确认任务，标记完成）"""
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

    # exclude_unset=True 表示只更新用户传过来的字段
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
