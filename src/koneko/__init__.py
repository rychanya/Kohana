from asyncio import Event, sleep
from collections.abc import AsyncIterable

from blacksheep import Application, Request, Response, get, html
from blacksheep.server.process import is_stopping
from blacksheep.server.sse import ServerSentEvent, ServerSentEventsResponse

app = Application()


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


async def stop_checker(request: Request, stop_event: Event):
    while True:
        if is_stopping():
            stop_event.set()
        if await request.is_disconnected():
            stop_event.set()
        await sleep(1)


async def sse_generator() -> AsyncIterable[ServerSentEvent]:
    await sleep(0)
    yield ServerSentEvent(data="1")


@get("/events")
async def events(request: Request):
    return ServerSentEventsResponse(events_provider=sse_generator)
