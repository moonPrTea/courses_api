from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, INTEGER, ForeignKey

from .base import Base

class Content(Base): # --> включает в себя весь контент курса
    __tablename__ = "content"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    content_type_id: Mapped[int] = mapped_column(ForeignKey("content_types.id"))
    text: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    order: Mapped[int] = mapped_column(INTEGER, nullable=True) # --> если Null, то рандомная цифра