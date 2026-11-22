# app/api/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.schemas import task_schema
from app.services import task_service

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


# ==========================================
# 1. 与 AI 对话并提取任务
# ==========================================
@router.post("/chat", summary="与 AI 助手对话并提取任务")
def chat_with_ai(
    req: ChatRequest, current_user_id: str = "1", db: Session = Depends(get_db)
):
    """用户通过自然语言对话，直接让 AI 创建任务"""
    result = task_service.process_chat_to_task(
        db, chat_text=req.message, user_id=int(current_user_id)
    )
    return result


# ==========================================
# 2. 获取智能收件箱（候选任务列表）
# ==========================================
@router.get(
    "/candidates",
    response_model=List[task_schema.TaskResponse],
    summary="获取 AI 提取的候选任务",
)
def get_candidates(current_user_id: str = "1", db: Session = Depends(get_db)) -> Any:
    tasks = task_service.get_tasks_by_status(
        db, user_id=int(current_user_id), status="CANDIDATE"
    )
    return tasks


# ==========================================
# 3. 获取任务看板（按状态获取列表）
# ==========================================
@router.get(
    "/", response_model=List[task_schema.TaskResponse], summary="获取任务看板列表"
)
def get_tasks(
    status: str = "IN_PROGRESS",
    current_user_id: str = "1",
    db: Session = Depends(get_db),
) -> Any:
    tasks = task_service.get_tasks_by_status(
        db, user_id=int(current_user_id), status=status
    )
    return tasks


# ==========================================
# 4. 确认任务（收件箱 -> 任务看板）
# ==========================================
@router.post("/{task_id}/confirm", summary="确认任务并加入看板")
def confirm_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="IN_PROGRESS"
    )
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"code": 200, "message": f"任务 {task_id} 已确认"}


# ==========================================
# 5. 标记任务完成
# ==========================================
@router.post("/{task_id}/complete", summary="标记任务为已完成")
def complete_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="COMPLETED"
    )
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"code": 200, "message": f"任务 {task_id} 已完成"}


# ==========================================
# 6. 删除/忽略任务
# ==========================================
@router.delete("/{task_id}", summary="删除或忽略任务")
def delete_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="DELETED"
    )
    if not success:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"code": 200, "message": f"任务 {task_id} 已删除"}


# ==========================================
# 7. 人工改写任务
# ==========================================
@router.put(
    "/{task_id}", response_model=task_schema.TaskResponse, summary="人工改写任务内容"
)
def edit_task(
    task_id: int,
    task_in: task_schema.TaskUpdate,
    current_user_id: str = "1",
    db: Session = Depends(get_db),
) -> Any:
    updated_task = task_service.update_task_info(
        db, task_id=task_id, user_id=int(current_user_id), task_in=task_in
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return updated_task
