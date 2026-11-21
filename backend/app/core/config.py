# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    # ==========================
    # 1. 基础项目配置
    # ==========================
    PROJECT_NAME: str = "AI 智能邮件任务助手"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # ==========================
    # 2. 数据库配置 (SQLite)
    # ==========================
    # 使用 SQLite，不需要账号密码，直接指定文件路径
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./ai_memo.db"

    # ==========================
    # 3. AI 大模型配置 (DeepSeek)
    # ==========================
    # 定义这个字段，Pydantic 才能从 .env 里读取到
    DEEPSEEK_API_KEY: str = "sk-xxxxxxxxxxxxxxxx"

    # ==========================
    # 4. 安全与跨域配置
    # ==========================
    SECRET_KEY: str = "super_secret_key_for_ai_memo_2026"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # ==========================
    # 5. 配置文件读取设置
    # ==========================
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        # 【核心修改】extra="ignore" 表示如果 .env 里有其他没定义过的变量，直接忽略，绝不报错
        extra="ignore",
    )


# 实例化全局配置
settings = Settings()
