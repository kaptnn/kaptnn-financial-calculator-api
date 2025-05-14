from fastapi import FastAPI
import uvicorn
from app.core.config import configs
from app.routes.routes import routers as v1_routers
from app.core.container import Container
from app.core.middleware import register_middleware

app = FastAPI()

class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="KAP TNN Calculator API",
            version="1.5.0",
            description="KAP TNN Calculator API Version 1.5.1",
            docs_url=f"{configs.API_PREFIX}/docs",
            redoc_url=f"{configs.API_PREFIX}/redoc",
            openapi_url=f"{configs.API_PREFIX}/openapi"
        )

        self.container = Container()
        self.db = self.container.db()

        register_middleware(self.app)

        @self.app.get(f"{configs.API_PREFIX}/health", tags=["Health Check"])
        async def root() -> dict:
            return {"message": "Welcome to KAP TNN Calculator API"}

        self.app.include_router(v1_routers, prefix=configs.API_PREFIX)

app = App().app

if __name__ == "__main__":
    try: 
        config = uvicorn.Config(app=app, reload=True)
        server = uvicorn.Server(config=config)
        server.run()
    except Exception as e:
        raise e
