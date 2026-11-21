# app/models/message.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    # 主键改为 Integer
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, comment="邮件ID"
    )

    # 外键保持 BigInteger 或 Integer 都可以，这里统一用 Integer
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, comment="所属用户ID"
    )

    sender_name = Column(String(100), comment="发件人")
    subject = Column(String(255), nullable=True, comment="邮件主题")
    content = Column(Text, nullable=False, comment="邮件正文")

    is_processed = Column(
        Integer, default=0, comment="处理状态：0未处理，1已处理，2忽略"
    )

    msg_time = Column(DateTime, nullable=False, comment="邮件接收时间")
    created_at = Column(DateTime, default=datetime.utcnow, comment="入库时间")

    user = relationship("User", backref="messages")
