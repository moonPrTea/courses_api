from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR

from .base import Base

class UserStatus(Base):
    __tablename__ = "user_status"
    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(VARCHAR)