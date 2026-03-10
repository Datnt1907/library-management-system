from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .book import Book


class Genre(RecordModel):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=True)

    books: Mapped[list["Book"]] = relationship(
        "Book", secondary="genre_books", back_populates="genres"
    )
