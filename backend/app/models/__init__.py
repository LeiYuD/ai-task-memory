# app/models/__init__.py

# 1. 统一从 database.py 导入唯一的 Base 和 engine
from app.core.database import Base, engine

# 2. 导入所有的数据模型，让 SQLAlchemy 能够识别它们
from app.models.user import User
from app.models.message import Message
from app.models.task import Task
from app.models.setting import Setting

# 3. 导出，供外部使用
__all__ = ["Base", "engine", "User", "Message", "Task", "Setting"]
