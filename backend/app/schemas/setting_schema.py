# app/schemas/setting_schema.py

from pydantic import BaseModel, Field
from typing import Optional


# ==========================================
# 1. 更新配置 (用于用户修改配置)
# ==========================================
class SettingUpdate(BaseModel):
    # 监控白名单，前端传 JSON 字符串过来，例如 '["工作群", "导师"]'
    target_groups: Optional[str] = Field(
        None, description="监控白名单（JSON格式字符串）"
    )
    ai_threshold: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="AI推送阈值(0-1之间)"
    )


# ==========================================
# 2. 返回配置 (用于前端读取配置)
# ==========================================
class SettingResponse(BaseModel):
    id: int
    user_id: int
    target_groups: str
    ai_threshold: float

    # 允许从 SQLAlchemy 模型对象直接转为 Pydantic 模型
    model_config = {"from_attributes": True}
