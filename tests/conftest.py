from collections.abc import AsyncIterator

import pytest
from koneko import app
from litestar import Litestar
from litestar.testing import AsyncTestClient


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def test_client() -> AsyncIterator[AsyncTestClient[Litestar]]:
    async with AsyncTestClient(app=app) as client:
        yield client
