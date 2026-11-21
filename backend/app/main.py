# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# 导入核心配置和组件
from app.core.config import settings
from app.api import api_router  # 汇总后的 API 路由
from app.core.database import engine
from app.models import Base

# 导入定时任务
from app.jobs import start_scheduler, stop_scheduler


# ==========================================
# 1. 生命周期管理 (Lifespan)
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 【启动时执行】
    print("=" * 50)
    print("🚀 AI 智能备忘录系统正在启动...")

    # 1. 自动创建数据库表 (对于 SQLite，第一次运行会自动生成 ai_memo.db)
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表结构同步完成")

    # 2. 启动后台定时任务 (轮询微信消息并调用 AI)
    start_scheduler()

    print("=" * 50)

    yield  # 这里是应用运行期间

    # 【关闭时执行】
    print("🛑 系统正在关闭...")
    stop_scheduler()


# ==========================================
# 2. 初始化 FastAPI 应用
# ==========================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="基于大语言模型的微信聊天记录任务提取与备忘录系统后端 API",
    version="1.0.0",
    lifespan=lifespan,
)

# ==========================================
# 3. 配置跨域 (CORS)
# ==========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有域名，部署时可改为前端具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 4. 注册路由 (Routers)
# ==========================================
# 将 app/api/__init__.py 里汇总的路由挂载到 /api/v1 前缀下
app.include_router(api_router, prefix="/api/v1")


# ==========================================
# 5. 根路由 (健康检查)
# ==========================================
@app.get("/", tags=["系统状态"])
async def root():
    return {
        "status": "online",
        "project_name": settings.PROJECT_NAME,
        "message": "服务运行正常，请访问 /docs 查看接口文档",
    }


# ==========================================
# 6. 本地开发启动入口
# ==========================================
if __name__ == "__main__":
    # 如果你在本地直接运行 `python app/main.py`，会启动服务
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
