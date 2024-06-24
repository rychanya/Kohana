import os

import uvicorn

if __name__ == "__main__":
    os.environ["APP_SIGNAL_HANDLER"] = "1"
    uvicorn.run("koneko:app")
