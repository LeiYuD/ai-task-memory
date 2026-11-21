# app/jobs/sync_email.py

import os
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from imapclient import IMAPClient
import mailparser
from dotenv import load_dotenv

# 强制加载 .env
load_dotenv()

from app.core.database import SessionLocal
from app.models.message import Message
from app.services.msg_service import process_message_with_ai

scheduler = BackgroundScheduler()


def fetch_real_qq_emails(db: Session):
    """基于时间戳增量拉取 QQ 邮箱"""
    user = os.getenv("QQ_EMAIL_ACCOUNT")
    password = os.getenv("QQ_EMAIL_AUTH_CODE")

    if not user or not password:
        print("⚠️ 未配置 QQ 邮箱账号或授权码，跳过真实拉取。")
        return

    # 核心逻辑：找出本地数据库里最新的一封邮件的时间
    last_msg = db.query(Message).order_by(Message.msg_time.desc()).first()

    if last_msg:
        since_date = last_msg.msg_time
        print(
            f"[Job] 本地最新记录为 {since_date.strftime('%Y-%m-%d %H:%M:%S')}，将从该时间开始增量拉取。"
        )
    else:
        # 如果本地是空的，为了演示，我们只拉取最近 3 天的邮件
        since_date = datetime.now() - timedelta(days=3)
        print(f"[Job] 本地无记录，初始化拉取最近 3 天的邮件。")

    try:
        with IMAPClient("imap.qq.com", ssl=True, use_uid=True) as server:
            server.login(user, password)
            server.select_folder("INBOX")

            # IMAP 的时间搜索格式必须是: 日-月-年 (例如 21-Nov-2026)
            imap_date_str = since_date.strftime("%d-%b-%Y")

            # 搜索：从指定日期开始的所有邮件
            messages = server.search(["SINCE", imap_date_str])
            if not messages:
                print("[Job] 📧 自上次同步以来，没有新邮件。")
                return

            print(f"[Job] 找到 {len(messages)} 封可能相关的邮件，开始解析...")

            # 取最新的 5 封（防止一次解析太多）
            for uid in messages[-5:]:
                raw_message = server.fetch([uid], ["RFC822"])[uid][b"RFC822"]
                mail = mailparser.parse_from_bytes(raw_message)

                subject = mail.subject or "无主题"
                sender = mail.from_[0][1] if mail.from_ else "未知发件人"
                body = (
                    mail.body.replace("\r\n", " ").replace("\n", " ")[:2000]
                    if mail.body
                    else "无正文"
                )

                # 获取邮件真实时间，如果解析失败则用当前时间
                msg_time = mail.date if mail.date else datetime.now()

                # 去重（防止同一时间段内的重复邮件）
                exists = (
                    db.query(Message)
                    .filter(Message.subject == subject, Message.sender_name == sender)
                    .first()
                )
                if exists:
                    continue

                new_msg = Message(
                    user_id=1,
                    sender_name=sender[:50],
                    subject=subject[:255],
                    content=body,
                    msg_time=msg_time,
                    is_processed=0,
                )
                db.add(new_msg)
                db.commit()
                print(f"[Job] 📧 成功拉取新邮件: {subject} (来自: {sender})")

    except Exception as e:
        print(f"❌ 邮箱拉取失败: {e}")


def scan_and_extract_tasks():
    """定时执行的核心任务"""
    print(f"--- [定时任务] 开始扫描收件箱 {datetime.now().strftime('%H:%M:%S')} ---")

    db = SessionLocal()
    try:
        # 1. 抓取真实邮件
        fetch_real_qq_emails(db)

        # 2. 调用 AI 提取任务
        unprocessed_msgs = db.query(Message).filter(Message.is_processed == 0).all()
        for msg in unprocessed_msgs:
            process_message_with_ai(db, msg, user_threshold=0.5)

    except Exception as e:
        print(f"[Job] 任务提取发生错误: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler.add_job(
        scan_and_extract_tasks,
        "interval",
        seconds=60,
        id="email_sync_job",
        replace_existing=True,
    )
    scheduler.start()
    print("✅ 真实 QQ 邮箱同步任务已启动 (每 60 秒检查一次)")


def stop_scheduler():
    scheduler.shutdown()
    print("🛑 定时任务调度器已关闭")
