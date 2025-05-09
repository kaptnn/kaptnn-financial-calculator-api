from fastapi import APIRouter
from app.routes.endpoints.calculator import router as calculator_router
from app.routes.endpoints.goal_seeking import router as goal_seeking_router
from app.routes.endpoints.auth import router as auth_router
from app.routes.endpoints.user import router as user_router
from app.routes.endpoints.company import router as company_router
from app.routes.endpoints.docs_category import router as docs_category_router
from app.routes.endpoints.docs_request import router as docs_request_router
from app.routes.endpoints.docs_manager import router as docs_manager_router
from app.routes.endpoints.docs import router as docs_router
from app.services.docs_manager.docs_service import DocsService

routers = APIRouter()
router_list = [
    auth_router, 
    user_router, 
    calculator_router, 
    goal_seeking_router, 
    company_router, 
    docs_category_router, 
    docs_request_router, 
    docs_manager_router, 
    docs_router,
]

for router in router_list:
    routers.include_router(router)