from datetime import datetime
from uuid import uuid4

from blacksheep import Request, Response, Router, html
from blacksheep.server.sse import ServerSentEvent, ServerSentEventsResponse

from koneko import SSEWrapper, events_list, queue_wrapper

router = Router()


@router.get("/")
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


@router.get("/events")
async def events(request: Request):
    queue = queue_wrapper.add(f"{uuid4()}")
    wrapper = SSEWrapper(request=request, queue=queue)
    return ServerSentEventsResponse(events_provider=wrapper.generator)


@router.post("/")
async def create_event():
    event = ServerSentEvent(data=f"event at {datetime.now()}")
    events_list.append(event)
    for queue in queue_wrapper.queryset.values():
        await queue.put(event)
    return "ok"
