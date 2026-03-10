from collections.abc import Sequence
from typing import Any
from uuid import UUID

from source.author.repository import AuthorRepository
from source.author.schemas import AuthorCreate, AuthorUpdate
from source.exceptions import ResourceNotFound
from source.models.author import Author
from source.postgres import AsyncSession


class AuthorNotFound(ResourceNotFound):
    def __init__(self) -> None:
        self.message = "Author not found"
        super().__init__(self.message)


class AuthorService:
    async def list(
        self,
        session: AsyncSession,
    ) -> Sequence[Author]:
        repository = AuthorRepository.from_session(session)
        statement = repository.get_base_statement()
        return await repository.get_all(statement)

    async def get(self, session: AsyncSession, id: UUID) -> Any:
        repository = AuthorRepository.from_session(session)
        author = await repository.get_by_id(id)
        if author is None:
            raise AuthorNotFound()
        return author

    async def create(
        self, session: AsyncSession, author_create: AuthorCreate
    ) -> Author:
        repository = AuthorRepository.from_session(session)
        author = await repository.create(
            Author(
                name=author_create.name,
                email=author_create.email,
                biography=author_create.biography,
            ),
            flush=True,
        )
        return author

    async def update(
        self, session: AsyncSession, id: UUID, author_update: AuthorUpdate
    ) -> Author:
        repository = AuthorRepository.from_session(session)
        author = await repository.get_by_id(id)
        if author is None:
            raise AuthorNotFound()
        author = await repository.update(
            author,
            update_dict=author_update.model_dump(exclude_unset=True),
        )
        return author


author_service = AuthorService()
