from datetime import datetime, timedelta
from typing import Optional, Any
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

# 1. 密码加密上下文 (使用 bcrypt 算法)
# 虽然本项目可能是单用户，但保留密码加密逻辑是基础规范
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 2. OAuth2 鉴权方案，告诉 FastAPI 从哪里获取 Token
# tokenUrl 填你后面写的登录接口路径
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


# ==========================================
# 密码加密与校验
# ==========================================
def get_password_hash(password: str) -> str:
    """将明文密码加密"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """校验明文密码和哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# 生成与解析 JWT Token
# ==========================================
def create_access_token(
    subject: str | Any, expires_delta: Optional[timedelta] = None
) -> str:
    """生成 JWT 访问令牌"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    # 将用户信息和过期时间打包
    to_encode = {"exp": expire, "sub": str(subject)}
    # 使用密钥进行签名
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# ==========================================
# 依赖注入：获取当前登录用户
# ==========================================
async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """
    核心鉴权依赖：用于保护需要登录才能访问的接口。
    如果 Token 无效，直接抛出 401 异常。
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="登录状态已失效，请重新登录",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解析 Token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
