import random
import string

from source.models.author import Author
from tests.fixtures.database import SaveFixture


def rstr(prefix: str) -> str:
    return prefix + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


async def create_author(
    save_fixture: SaveFixture,
) -> Author:
    dump_author_name = rstr("test_author")
    author = Author(
        name=dump_author_name,
        email=f"{dump_author_name}@gmail.com",
        biography="Test biography",
    )
    await save_fixture(author)
    return author
