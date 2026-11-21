# app/jobs/__init__.py

from .sync_email import start_scheduler, stop_scheduler

__all__ = ["start_scheduler", "stop_scheduler"]
