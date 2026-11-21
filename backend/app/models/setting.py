# app/models/setting.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Setting(Base):
    __tablename__ = "settings"

    # 主键改为 Integer
    id = Column(
        Integer, primary_key=True, index=True, autoincrement=True, comment="配置ID"
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        comment="所属用户ID",
    )

    target_groups = Column(String(500), default="[]", comment="监控白名单（JSON格式）")
    ai_threshold = Column(Float, default=0.7, comment="AI推送阈值")

    user = relationship("User", backref="setting", uselist=False)
