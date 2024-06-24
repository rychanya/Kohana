import pytest
from httpx_sse import aconnect_sse
from litestar import Litestar
from litestar.status_codes import HTTP_200_OK
from litestar.testing import AsyncTestClient

pytestmark = pytest.mark.anyio


async def test_health_check(test_client: AsyncTestClient[Litestar]):
    response = await test_client.get("/")
    assert response.status_code == HTTP_200_OK
    assert response.text == "Hello, world!"


async def test_sse(test_client: AsyncTestClient[Litestar]):
    async with aconnect_sse(client=test_client, method="GET", url="/events") as event_source:
        sse_iter = event_source.aiter_sse()
        sse = await anext(sse_iter)
        assert sse.data == "test"

        # sse2 = await anext(sse_iter)
        # assert sse2.data == "test_2"
