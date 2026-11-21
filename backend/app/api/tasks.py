# app/api/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from sqlalchemy.orm import Session

# 注释掉安全模块
# from app.core.security import get_current_user
from app.core.database import get_db
from app.schemas import task_schema
from app.services import task_service

router = APIRouter()


# ==========================================
# 1. 获取智能收件箱（候选任务列表）
# ==========================================
@router.get(
    "/candidates",
    response_model=List[task_schema.TaskResponse],
    summary="获取 AI 提取的候选任务",
)
def get_candidates(
    # 直接给定默认值 "1"，绕过鉴权
    current_user_id: str = "1",
    db: Session = Depends(get_db),
) -> Any:
    tasks = task_service.get_tasks_by_status(
        db, user_id=int(current_user_id), status="CANDIDATE"
    )
    return tasks


# ==========================================
# 2. 确认任务（收件箱 -> 任务看板）
# ==========================================
@router.post("/{task_id}/confirm", summary="确认任务并加入看板")
def confirm_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="IN_PROGRESS"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return {"code": 200, "message": f"任务 {task_id} 已确认，已加入任务看板"}


# ==========================================
# 3. 人工改写任务
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return updated_task


# ==========================================
# 4. 获取任务看板（按状态获取列表）
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
