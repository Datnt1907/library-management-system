from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .book import Book


class Inventory(RecordModel):
    __tablename__ = "inventories"

    shelf_location: Mapped[str] = mapped_column(String(100), nullable=False)
    total_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    available_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    book_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("books.id", ondelete="cascade"), nullable=False
    )

    book: Mapped["Book"] = relationship("Book", back_populates="inventories")
