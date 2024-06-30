from asyncio import Queue, TimeoutError, wait_for
from collections.abc import AsyncIterable
from datetime import datetime

from blacksheep import Request
from blacksheep.server.process import is_stopping
from blacksheep.server.sse import ServerSentEvent

events_list: list[ServerSentEvent] = list()


class SSEWrapper:
    def __init__(self, request: Request, queue: Queue[ServerSentEvent], timeout: int = 1) -> None:
        self._request = request
        self.queue = queue
        self.timeout = timeout

    async def is_connected(self) -> bool:
        return not (is_stopping() or await self._request.is_disconnected())

    async def generator(self) -> AsyncIterable[ServerSentEvent]:
        while await self.is_connected():
            try:
                yield await wait_for(self.queue.get(), self.timeout)
            except TimeoutError:
                yield ServerSentEvent(data=f"{datetime.now()}", event="ping")


class QueueWrapper:
    def __init__(self) -> None:
        self.queryset: dict[str, Queue[ServerSentEvent]] = dict()

    def add(self, key: str) -> Queue[ServerSentEvent]:
        queue: Queue[ServerSentEvent] = Queue()
        self.queryset[key] = queue
        return queue


queue_wrapper = QueueWrapper()
