import pytest

from source.author.schemas import AuthorUpdate
from source.author.service import author_service
from source.postgres import AsyncSession
from tests.fixtures.database import SaveFixture
from tests.fixtures.random_objects import create_author


@pytest.mark.asyncio
class TestAuthorService:
    async def test_update_author(
        self, save_fixture: SaveFixture, session: AsyncSession
    ) -> None:
        author = await create_author(save_fixture)

        updated_author = await author_service.update(
            session, author.id, author_update=AuthorUpdate(name="Updated Name")
        )

        assert updated_author.name == "Updated Name"
