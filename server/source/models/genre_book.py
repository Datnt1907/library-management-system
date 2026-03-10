from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from source.kit.db.models import TimestampedModel


class GenreBook(TimestampedModel):
    __tablename__ = "genre_books"

    genre_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("genres.id", ondelete="cascade"),
        primary_key=True,
    )
    book_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("books.id", ondelete="cascade"),
        primary_key=True,
    )
