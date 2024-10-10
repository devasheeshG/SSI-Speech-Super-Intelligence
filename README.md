@mayank https://www.markepear.com/blog/github-search-engine-optimization

https://www.codemotion.com/magazine/dev-life/github-project/

usecase 1 - use in existing repos
all models will be loaded from the existing repo and then the server will be started

```python
from fastapi import FastAPI
from ssi.fastapi.routers import StreamingWSRouter
from ssi.types import StreamingDataChunk

app = FastAPI()

def callback(data: StreamingDataChunk):
    print(data)

streaming_ws_router = StreamingWSRouter(
    callback=callback,
)

app.include_router(streaming_ws_router)
```

usecase 2 - deploy as a docker server and then use in existing repos
here SSI server is deployed as a docker container and then ssi_client can be used in existing repos

```python
from fastapi import FastAPI
from ssi.clients import StreamingClient
from ssi.types import StreamingDataChunk

app = FastAPI()

def callback(data: StreamingDataChunk):
    print(data)

ssi_client = StreamingClient(
    server_host="localhost",
    server_port=8000,
    callback=callback,
)

app.include_router(ssi_client.fastapi_proxy_router)
```

usecase 3 - CLI (for local system as well as simple socket server)
bc dimak nhi chal rha abhi
