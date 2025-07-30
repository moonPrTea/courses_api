from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import VARCHAR

from .base import Base

class ContentTypes(Base):
    __tablename__ = "content_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR)