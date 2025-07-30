
from sqlalchemy import VARCHAR, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum as SQLEnum
from enum import Enum as PyEnum

from .base import Base

class OrderEnum(PyEnum): # --> enum для порядка подсказок
    first = 1
    second = 2
    third = 3
    default = 0

class Hints(Base): 
    __tablename__ = "hints"
    id: Mapped[int] = mapped_column(primary_key=True)
    content_id: Mapped[str] = mapped_column(ForeignKey("content.id"))
    text: Mapped[str] = mapped_column(VARCHAR)
    order: Mapped[OrderEnum] = mapped_column(
        SQLEnum(OrderEnum),
        nullable=False,
        default=OrderEnum.default
    )
    