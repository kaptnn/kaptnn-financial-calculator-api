from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import configs
from app.routes.routes import routers as v1_routers
from app.utils.pattern import singleton
from app.core.container import Container

app = FastAPI()

@singleton
class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="KAP TNN Calculator API",
            version="1.1.0",
        )

        self.container = Container()
        self.db = self.container.db()

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        @self.app.get("/")
        def root():
            return {"message": "Welcome to KAP TNN Calculator API " + configs.DB_URI}
        
        self.app.include_router(v1_routers, prefix=configs.API_PREFIX)
        
app_instance = App()
app = app_instance.app
