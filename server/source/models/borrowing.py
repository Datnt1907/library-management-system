from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import TIMESTAMP, ForeignKey, Uuid
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .book import Book
    from .user import User


class BorrowingStatus(Enum):
    BORROWED = "borrowed"
    RETURNED = "returned"
    OVERDUE = "overdue"


class Borrowing(RecordModel):
    __tablename__ = "borrowings"

    borrow_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    return_date: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    due_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    status: Mapped[BorrowingStatus] = mapped_column(
        SAEnum(BorrowingStatus, name="borrow_status"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="cascade"), nullable=False
    )
    book_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("books.id", ondelete="cascade"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="borrowings")
    book: Mapped["Book"] = relationship("Book", back_populates="borrowings")
