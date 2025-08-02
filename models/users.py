from fastapi import Depends
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR, BOOLEAN, ForeignKey, TIMESTAMP, LargeBinary, select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from .base import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR)
    password: Mapped[str] = mapped_column(LargeBinary(32)) # --> с хешем
    salt: Mapped[str] = mapped_column(LargeBinary(32))
    email: Mapped[str] = mapped_column(VARCHAR)
    description: Mapped[str] = mapped_column(VARCHAR, nullable=True)
    user_status_id: Mapped[str] = mapped_column(ForeignKey("user_status.id"), nullable=True)
    active: Mapped[bool] = mapped_column(BOOLEAN, default=True)
    created_at: Mapped[str] = mapped_column(TIMESTAMP(timezone=False), server_default=func.now())
    admin: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    
    @classmethod
    async def create_user(
        cls,
        username: str, email: str, psw: bytes, salt: bytes,
        session: AsyncSession
    ) -> int:
        new_user = cls(username=username, email=email, password=psw, salt=salt)
        print(new_user)
        session.add(new_user)
        await session.commit()
        
        await session.refresh(new_user)
        
        print(f"результат добавления - {new_user}")
        
        return new_user.id