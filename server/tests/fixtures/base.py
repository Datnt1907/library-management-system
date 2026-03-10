from collections.abc import AsyncGenerator
from typing import Any

import httpx
import pytest
import pytest_asyncio
from fastapi import FastAPI

from source.app import app as library_management_app
from source.postgres import AsyncSession, get_db_session


class IsolatedSessionTestClient(httpx.AsyncClient):
    """
    Test client that mimics production behavior by clearing session before requests.

    In production, each HTTP request gets a fresh database session. This client
    simulates that by expunging all objects from the test session before each
    request, catching lazy='raise' errors that would otherwise pass in tests.

    Disable for specific tests with @pytest.mark.keep_session_state marker.
    """

    def __init__(
        self, session: AsyncSession, auto_expunge: bool, *args: Any, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self._session = session
        self._auto_expunge = auto_expunge

    async def request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        """Expunge session before each request to simulate production."""
        if self._auto_expunge:
            self._session.expunge_all()
        return await super().request(*args, **kwargs)


@pytest_asyncio.fixture
async def app(session: AsyncSession) -> AsyncGenerator[FastAPI]:
    library_management_app.dependency_overrides[get_db_session] = lambda: session

    yield library_management_app

    library_management_app.dependency_overrides.pop(get_db_session)


@pytest_asyncio.fixture
async def client(
    app: FastAPI, session: AsyncSession, request: pytest.FixtureRequest
) -> AsyncGenerator[httpx.AsyncClient, None]:
    async with IsolatedSessionTestClient(
        session=session,
        auto_expunge=True,
        transport=httpx.ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client
