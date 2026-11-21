# app/models/user.py

from sqlalchemy import Column, BigInteger, String, DateTime
from datetime import datetime
from . import Base  # 从 __init__.py 导入 Base


class User(Base):
    __tablename__ = "users"

    # 主键
    id = Column(
        BigInteger, primary_key=True, index=True, autoincrement=True, comment="用户ID"
    )

    # 基本信息
    nickname = Column(String(50), nullable=False, comment="用户昵称")
    wx_id = Column(
        String(100), unique=True, index=True, nullable=False, comment="绑定的微信标识"
    )

    # 时间
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
