# app/api/__init__.py

from fastapi import APIRouter

# 1. 导入各个子模块的路由实例
# 注意：这里假设你在 tasks.py 和 settings.py 中定义的变量名是 router
from app.api.tasks import router as tasks_router
from app.api.settings import router as settings_router

# 2. 创建一个主路由 (不带前缀，前缀在 main.py 中统一加)
api_router = APIRouter()

# 3. 把子路由挂载到主路由上
# 建议在这里给子路由加上 tags，这样在 Swagger 文档里会自动分类
api_router.include_router(tasks_router, prefix="/tasks", tags=["任务管理"])
api_router.include_router(settings_router, prefix="/settings", tags=["配置管理"])

# 如果你还有消息相关的接口，可以继续加：
# from app.api.messages import router as messages_router
# api_router.include_router(messages_router, prefix="/messages", tags=["消息管理"])

# 4. 导出主路由供 main.py 使用
__all__ = ["api_router"]
