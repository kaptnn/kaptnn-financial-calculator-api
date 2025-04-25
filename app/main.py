from fastapi import FastAPI
from app.core.config import configs
from app.routes.routes import routers as v1_routers
from app.utils.pattern import singleton
from app.core.container import Container
from app.core.middleware import register_middleware

app = FastAPI()

@singleton
class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="KAP TNN Calculator API",
            docs_url=f"{configs.API_PREFIX}/docs",
            redoc_url=f"{configs.API_PREFIX}/redoc",
            version="1.5.0",
        )

        self.container = Container()
        self.db = self.container.db()

        register_middleware(self.app)
        
        @self.app.get(f"{configs.API_PREFIX}/health", tags=["Health Check"])
        async def root() -> dict:
            return {"message": "Welcome to KAP TNN Calculator API"}
        
        self.app.include_router(v1_routers, prefix=configs.API_PREFIX)
        
app_instance = App()
app = app_instance.app
