from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models.base import RecordModel

if TYPE_CHECKING:
    from .book import Book


class Author(RecordModel):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    biography: Mapped[str] = mapped_column(String(250), nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary="author_books", back_populates="authors"
    )
