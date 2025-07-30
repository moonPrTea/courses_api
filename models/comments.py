from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, ForeignKey

from .base import Base

class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(VARCHAR)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    