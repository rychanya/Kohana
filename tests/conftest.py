from collections.abc import AsyncIterator

import httpx
import pytest
from koneko.app import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
async def test_client() -> AsyncIterator[httpx.AsyncClient]:
    await app.start()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
    await app.stop()
