import os

import uvicorn

from koneko.app import app

if __name__ == "__main__":
    os.environ["APP_SIGNAL_HANDLER"] = "1"
    uvicorn.run(app=app)
