from contextlib import asynccontextmanager
from fastapi import FastAPI
import ngrok
import uvicorn
from app.core.config import configs
from app.routes.routes import routers as v1_routers
from app.core.container import Container
from app.core.middleware import register_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    if configs.ENV == "development":
        ngrok.set_auth_token(configs.NGROK_AUTHTOKEN)
        print(f"Setting up Ngrok Tunnel on {configs.NGROK_DOMAIN}")
        tunnel = ngrok.forward(
            addr=8000,
            domain=configs.NGROK_DOMAIN
        )
    yield
    if configs.ENV == "development" and tunnel:
        print("Tearing Down Ngrok Tunnel")
        ngrok.disconnect()

def create_app() -> FastAPI:
    app = FastAPI(
        title=configs.PROJECT_NAME,
        version="1.5.0",
        description=f"{configs.PROJECT_NAME} v1.5.1",
        docs_url=f"{configs.API_PREFIX}/docs",
        redoc_url=f"{configs.API_PREFIX}/redoc",
        openapi_url=f"{configs.API_PREFIX}/openapi.json",
        lifespan=lifespan
    )

    container = Container()
    container.db()

    register_middleware(app)

    @app.get(f"{configs.API_PREFIX}/health", tags=["Health Check"])
    async def health() -> dict:
        return {"message": "KAP TNN Calculator API is up and running!"}

    app.include_router(v1_routers, prefix=configs.API_PREFIX)

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=(configs.ENV == "development"),
        workers=1
    )