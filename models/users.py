from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, BOOLEAN, ForeignKey, TIMESTAMP

from .base import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    password: Mapped[str] = mapped_column(VARCHAR, nullable=False) # --> с хешем
    email: Mapped[str] = mapped_column(VARCHAR)
    description: Mapped[str] = mapped_column(VARCHAR)
    user_status_id: Mapped[str] = mapped_column(ForeignKey("user_status.id"))
    active: Mapped[bool] = mapped_column(BOOLEAN)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=False))
    admin: Mapped[bool] = mapped_column(BOOLEAN, default=False)