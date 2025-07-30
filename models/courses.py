from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, INTEGER, BOOLEAN, ForeignKey

from .base import Base

class Courses(Base): # --> информация о курсах
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(250)) 
    description: Mapped[str] = mapped_column(VARCHAR)
    level_id: Mapped[int] = mapped_column(ForeignKey("course_levels.id"))
    count_lessons: Mapped[int] = mapped_column(INTEGER, default=0)     
    number_of_participants: Mapped[int] = mapped_column(INTEGER, default=0)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=True)