from uuid import UUID

from source.kit.repository.base import (
    RepositoryBase,
    RepositorySoftDeletionIDMixin,
    RepositorySoftDeletionMixin,
)
from source.models.author import Author


class AuthorRepository(
    RepositorySoftDeletionIDMixin[Author, UUID],
    RepositorySoftDeletionMixin[Author],
    RepositoryBase[Author],
):
    model = Author
