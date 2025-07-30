from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR

from .base import Base

class CourseLevels(Base):
    __tablename__ = "course_levels"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR)
    