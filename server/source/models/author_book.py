from uuid import UUID

from sqlalchemy import ForeignKey, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from source.kit.db.models import TimestampedModel


class AuthorBook(TimestampedModel):
    __tablename__ = "author_books"

    author_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("authors.id", ondelete="cascade"),
        primary_key=True,
    )
    book_id: Mapped[UUID] = mapped_column(
        Uuid,
        ForeignKey("books.id", ondelete="cascade"),
        primary_key=True,
    )
