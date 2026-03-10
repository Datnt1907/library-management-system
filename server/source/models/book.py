from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .author import Author
    from .borrowing import Borrowing
    from .genre import Genre
    from .inventory import Inventory
    from .publisher import Publisher


class Book(RecordModel):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    publisher_year: Mapped[int] = mapped_column(Integer, nullable=False)
    publisher_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey("publishers.id", ondelete="cascade"), nullable=False
    )

    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="books")
    borrowings: Mapped[list["Borrowing"]] = relationship(
        "Borrowing", back_populates="book"
    )
    inventories: Mapped[list["Inventory"]] = relationship(
        "Inventory", back_populates="book"
    )
    genres: Mapped[list["Genre"]] = relationship(
        "Genre", secondary="genre_books", back_populates="books"
    )
    authors: Mapped[list["Author"]] = relationship(
        "Author", secondary="author_books", back_populates="books"
    )
