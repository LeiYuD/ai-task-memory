# backend/init_db.py

# 关键点1：强制在文件头部把所有相关的模型全部导入！
# 这样 SQLAlchemy 在内存中就会把所有表建好，彻底解决外键找不到表的问题
from app.core.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.message import Message
from app.models.task import Task
from app.models.setting import Setting


def init_data():
    print("正在初始化数据库...")
    # 建表
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        if not user:
            default_user = User(id=1, nickname="测试用户", wx_id="test_wx_id_001")
            db.add(default_user)

            default_setting = Setting(user_id=1, ai_threshold=0.7, target_groups="[]")
            db.add(default_setting)

            db.commit()
            print("✅ 默认用户和配置初始化成功！")
        else:
            print("✅ 数据库已有用户，跳过初始化。")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_data()
