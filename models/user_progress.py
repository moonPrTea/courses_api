from sqlalchemy import ForeignKey, BOOLEAN, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class UserProgress(Base): # --> будет использовано для получения статистики пользователей
    __tablename__ = "user_progress"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"))
    completed: Mapped[bool] = mapped_column(BOOLEAN)
    completed_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=False))