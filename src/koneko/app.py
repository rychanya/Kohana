from blacksheep import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info  # type: ignore

from koneko.routs import router

app = Application(router=router)
docs = OpenAPIHandler(info=Info(title="Example API", version="0.0.1"))
docs.bind_app(app)
