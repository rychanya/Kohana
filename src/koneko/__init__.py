from asyncio import Queue, TimeoutError, wait_for
from collections.abc import AsyncGenerator

from litestar import Litestar, Request, get, post
from litestar.response import ServerSentEvent, ServerSentEventMessage
from litestar.types import SSEData


@get(path="/")
async def index() -> str:
    return "Hello, world!"


async def generator(queue: Queue[ServerSentEventMessage], request: Request) -> AsyncGenerator[SSEData, None]:
    # yield ServerSentEventMessage(data="test")
    while True:
        print(1)
        try:
            yield await wait_for(queue.get(), 1)
        except TimeoutError:
            pass
        if not request.is_connected:
            break
    # yield await queue.get()


@get(path="/events")
async def events(request: Request) -> ServerSentEvent:
    queue: Queue[ServerSentEventMessage] = Queue()
    await queue.put(ServerSentEventMessage(data="test"))
    await queue.put(ServerSentEventMessage(data="test_2"))
    return ServerSentEvent(generator(queue, request))


@post(path="/events")
async def create_event() -> str:
    return "new event"


app = Litestar(route_handlers=[index, events, create_event])
