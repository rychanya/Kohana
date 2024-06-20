from collections.abc import AsyncGenerator

from litestar import Litestar, get
from litestar.response import ServerSentEvent, ServerSentEventMessage
from litestar.types import SSEData


@get(path="/")
async def index() -> str:
    return "Hello, world!"


async def generator() -> AsyncGenerator[SSEData, None]:
    yield ServerSentEventMessage(data="test")


@get(path="/events")
async def events() -> ServerSentEvent:
    return ServerSentEvent(generator())


app = Litestar(route_handlers=[index, events])
