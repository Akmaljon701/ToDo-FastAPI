from app.database import Base
from app.tasks import choices
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref
from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    body = Column(Text, nullable=False)
    status = Column(Enum(choices.TaskStatus), nullable=True, default=choices.TaskStatus.PENDING)
    execution_datetime = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref=backref("tasks", lazy="dynamic"))