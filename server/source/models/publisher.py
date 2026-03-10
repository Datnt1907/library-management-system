from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .book import Book


class Publisher(RecordModel):
    __tablename__ = "publishers"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    contact_number: Mapped[str] = mapped_column(String(50), nullable=True)

    books: Mapped[list["Book"]] = relationship("Book", back_populates="publisher")
