# app/api/__init__.py

from fastapi import APIRouter

# 1. 导入各个子模块的路由实例
from app.api.tasks import router as tasks_router
from app.api.settings import router as settings_router

# 2. 创建一个主路由
api_router = APIRouter()

# 3. 把子路由挂载到主路由上
# 任务管理
api_router.include_router(tasks_router, prefix="/tasks", tags=["任务管理"])

# 配置管理（只需挂载这一次！GET和PUT都在这个路由里）
api_router.include_router(settings_router, prefix="/settings", tags=["配置管理"])

__all__ = ["api_router"]
