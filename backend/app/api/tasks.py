# app/api/tasks.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from sqlalchemy.orm import Session

# 导入数据库、Schemas 和 Services
from app.core.database import get_db
from app.schemas import task_schema
from app.services import task_service

# 注意：为了演示方便，我们把 get_current_user 的鉴权去掉了，默认 user_id = 1

router = APIRouter()


# 辅助函数：将 ORM 对象转为 Pydantic 模型，并附带上来源邮件的时间
def build_task_response(task):
    # 强制把关联的 message 的 msg_time 赋值给 source_msg_time
    task_dict = task.__dict__.copy()
    if task.source_message:
        task_dict["source_msg_time"] = task.source_message.msg_time
    return task_dict


# ==========================================
# 1. 获取智能收件箱（候选任务列表）
# ==========================================
@router.get(
    "/candidates",
    response_model=List[task_schema.TaskResponse],
    summary="获取 AI 提取的候选任务",
)
def get_candidates(current_user_id: str = "1", db: Session = Depends(get_db)) -> Any:
    """获取状态为 CANDIDATE（候选）的任务列表"""
    tasks = task_service.get_tasks_by_status(
        db, user_id=int(current_user_id), status="CANDIDATE"
    )
    return tasks


# ==========================================
# 2. 获取任务看板（按状态获取列表）
# ==========================================
@router.get(
    "/", response_model=List[task_schema.TaskResponse], summary="获取任务看板列表"
)
def get_tasks(
    status: str = "IN_PROGRESS",  # 默认获取进行中的任务
    current_user_id: str = "1",
    db: Session = Depends(get_db),
) -> Any:
    """获取任务看板列表，支持通过 query 参数过滤状态"""
    tasks = task_service.get_tasks_by_status(
        db, user_id=int(current_user_id), status=status
    )
    return tasks


# ==========================================
# 3. 确认任务（收件箱 -> 任务看板）
# ==========================================
@router.post("/{task_id}/confirm", summary="确认任务并加入看板")
def confirm_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    """用户点击确认，任务状态从 CANDIDATE 变更为 IN_PROGRESS"""
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="IN_PROGRESS"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return {"code": 200, "message": f"任务 {task_id} 已确认，已加入任务看板"}


# ==========================================
# 4. 标记任务完成（看板 -> 已完成）
# ==========================================
@router.post("/{task_id}/complete", summary="标记任务为已完成")
def complete_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    """用户点击完成，任务状态从 IN_PROGRESS 变更为 COMPLETED"""
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="COMPLETED"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return {"code": 200, "message": f"任务 {task_id} 已标记为完成"}


# ==========================================
# 5. 删除/忽略任务
# ==========================================
@router.delete("/{task_id}", summary="删除或忽略任务")
def delete_task(
    task_id: int, current_user_id: str = "1", db: Session = Depends(get_db)
):
    """将任务状态标记为 DELETED（软删除）"""
    success = task_service.update_task_status(
        db, task_id=task_id, user_id=int(current_user_id), new_status="DELETED"
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return {"code": 200, "message": f"任务 {task_id} 已删除"}


# ==========================================
# 6. 人工改写任务
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
    """用户对 AI 提取的结果不满意，手动修改标题、截止时间等信息"""
    updated_task = task_service.update_task_info(
        db, task_id=task_id, user_id=int(current_user_id), task_in=task_in
    )

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="任务不存在或无权操作"
        )

    return updated_task
