# app/api/settings.py

from fastapi import APIRouter
import os

router = APIRouter()


# ==========================================
# 1. 你原本的更新配置接口 (保留)
# ==========================================
@router.put("/", summary="更新系统配置")
def update_settings():
    # 这里目前是假逻辑，等后续需要真正修改配置时再完善
    return {"message": "更新配置成功"}


# ==========================================
# 2. 新增的获取配置接口 (给前端弹窗用)
# ==========================================
@router.get("/", summary="获取系统配置状态")
def get_settings():
    # 从环境变量读取你的邮箱账号
    email = os.getenv("QQ_EMAIL_ACCOUNT", "未配置")

    # 简单的脱敏逻辑
    masked_email = email
    if "@" in email:
        parts = email.split("@")
        if len(parts[0]) > 3:
            masked_email = parts[0][:3] + "***@" + parts[1]
        else:
            masked_email = parts[0][0] + "***@" + parts[1]

    return {"email": email, "masked_email": masked_email}
