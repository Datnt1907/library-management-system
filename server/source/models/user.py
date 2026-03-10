from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from source.kit.db.models import RecordModel

if TYPE_CHECKING:
    from .borrowing import Borrowing


class User(RecordModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15))

    borrowings: Mapped[list["Borrowing"]] = relationship(
        "Borrowing", back_populates="user"
    )
