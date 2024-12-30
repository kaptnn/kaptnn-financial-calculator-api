from fastapi import APIRouter
from app.routes.endpoints.calculator import router as calculator_router
from app.routes.endpoints.goal_seeking import router as goal_seeking_router

routers = APIRouter()
router_list = [calculator_router, goal_seeking_router]

for router in router_list:
    routers.include_router(router)