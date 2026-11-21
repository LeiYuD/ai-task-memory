# app/models/task.py

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    # 主键改为 Integer
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, comment="任务ID"
    )

    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="所属用户ID"
    )
    source_msg_id = Column(
        Integer, ForeignKey("messages.id"), nullable=True, comment="来源消息ID"
    )

    title = Column(String(255), nullable=False, comment="任务标题")
    description = Column(Text, nullable=True, comment="详细描述")

    status = Column(
        String(20), default="CANDIDATE", nullable=False, index=True, comment="任务状态"
    )

    deadline = Column(DateTime, nullable=True, comment="截止时间")
    confidence = Column(Float, default=1.0, comment="AI抽取置信度 (0.00-1.00)")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")

    user = relationship("User", backref="tasks")
    source_message = relationship("Message", backref="derived_tasks")
