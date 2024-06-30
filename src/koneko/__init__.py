from asyncio import (
    Queue,
    TimeoutError,
    wait_for,
)
from collections.abc import AsyncIterable
from datetime import datetime
from uuid import uuid4

from blacksheep import Application, Request, Response, get, html, post
from blacksheep.server.openapi.v3 import OpenAPIHandler
from blacksheep.server.process import is_stopping
from blacksheep.server.sse import ServerSentEvent, ServerSentEventsResponse
from openapidocs.v3 import Info  # type: ignore

app = Application()
docs = OpenAPIHandler(info=Info(title="Example API", version="0.0.1"))
docs.bind_app(app)
events_list: list[ServerSentEvent] = list()


@get("/")
async def index() -> Response:
    res = """<html>
    <body>
        <div>
            <span>Hello World!</span>
        </div>
        <ul></ul>
    </body>
    <script>
        let eventSource;
        eventSource = new EventSource('/events');
        const eventList = document.querySelector("ul");

        eventSource.onmessage = (e) => {
            const newElement = document.createElement("li");
            newElement.textContent = `message: ${e.data}`;
            eventList.appendChild(newElement);
        };
    </script>
</html>"""
    return html(value=res)


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


@get("/events")
async def events(request: Request):
    queue = queue_wrapper.add(f"{uuid4()}")
    wrapper = SSEWrapper(request=request, queue=queue)
    return ServerSentEventsResponse(events_provider=wrapper.generator)


@post("/")
async def create_event():
    event = ServerSentEvent(data=f"event at {datetime.now()}")
    events_list.append(event)
    for queue in queue_wrapper.queryset.values():
        await queue.put(event)
    return "ok"
