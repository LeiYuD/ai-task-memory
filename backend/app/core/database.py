# app/core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 使用 SQLite 的连接字符串
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

# SQLite 需要 connect_args={"check_same_thread": False}
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
