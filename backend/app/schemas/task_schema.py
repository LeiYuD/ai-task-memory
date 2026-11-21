# app/schemas/task_schema.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==========================================
# 1. 基础 Schema (包含共有字段)
# ==========================================
class TaskBase(BaseModel):
    title: str = Field(..., description="任务标题", max_length=255)
    description: Optional[str] = Field(None, description="任务详细描述")
    deadline: Optional[datetime] = Field(None, description="截止时间")
    status: str = Field("CANDIDATE", description="任务状态")


# ==========================================
# 2. 创建任务 (用于 AI 提取后写入数据库)
# ==========================================
class TaskCreate(TaskBase):
    user_id: int = Field(..., description="所属用户ID")
    source_msg_id: Optional[int] = Field(None, description="来源消息ID")
    confidence: float = Field(1.0, description="AI置信度")


# ==========================================
# 3. 更新任务 (用于用户在收件箱【人工改写】)
# ==========================================
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, description="修改后的标题")
    description: Optional[str] = Field(None, description="修改后的描述")
    deadline: Optional[datetime] = Field(None, description="修改后的截止时间")
    status: Optional[str] = Field(None, description="修改状态 (如确认, 完成)")


# ==========================================
# 4. 返回任务 (用于给前端展示的数据)
# ==========================================
class TaskResponse(TaskBase):
    id: int
    user_id: int
    source_msg_id: Optional[int]
    confidence: float
    created_at: datetime

    # 允许从 SQLAlchemy 模型对象直接转为 Pydantic 模型
    model_config = {"from_attributes": True}
