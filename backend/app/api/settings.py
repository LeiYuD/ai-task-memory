from fastapi import APIRouter

router = APIRouter()


@router.put("/")
def update_settings():
    return {"message": "更新配置成功"}
