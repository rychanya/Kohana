import httpx
import pytest

pytestmark = pytest.mark.anyio


async def test_health_check(test_client: httpx.AsyncClient):
    r = await test_client.get("/")
    assert r.status_code == 200
    # response = await test_client.get("/")
    # assert response.status_code == HTTP_200_OK


# async def test_sse(test_client: TestClient):
#     async with aconnect_sse(client=test_client, method="GET", url="/events") as event_source:
#         sse_iter = event_source.aiter_sse()
#         sse = await anext(sse_iter)
#         assert sse.data == "test"

# sse2 = await anext(sse_iter)
# assert sse2.data == "test_2"
