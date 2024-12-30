from typing import Union
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.routes.routes import routers as v1_routers

app = FastAPI()

class App(FastAPI):
    def __init__(self):
        self.app: FastAPI = FastAPI(
            title="KAP TNN Calculator API",
            version="0.1.0",
        )

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

        @self.app.get("/")
        def root():
            return {"message": "Welcome to KAP TNN Calculator API"}
        
        self.app.include_router(v1_routers, prefix="/api/v1")
        
app_instance = App()
app = app_instance.app
