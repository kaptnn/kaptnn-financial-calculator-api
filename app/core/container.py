from dependency_injector import containers, providers
from app.core.config import configs
from app.core.database import Database
from app.repositories.user_repo import UserRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.docs_category_repo import DocsCategoryRepository
from app.repositories.docs_request_repo import DocsRequestRepository
from app.repositories.docs_repo import DocsRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.services.company_service import CompanyService
from app.services.docs_manager.docs_category_service import DocsCategoryService
from app.services.docs_manager.docs_request_service import DocsRequestService
from app.services.docs_manager.docs_service import DocsService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.routes.endpoints.auth",
            "app.routes.endpoints.user",
            "app.routes.endpoints.calculator",
            "app.routes.endpoints.goal_seeking",
            "app.routes.endpoints.company",
            "app.routes.endpoints.docs_category",
            "app.routes.endpoints.docs_request",
            "app.routes.endpoints.docs",
            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DB_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)
    company_repository = providers.Factory(CompanyRepository, session_factory=db.provided.session)
    docs_category_repository = providers.Factory(DocsCategoryRepository, session_factory=db.provided.session)
    docs_request_repository = providers.Factory(DocsRequestRepository, session_factory=db.provided.session)
    docs_repository = providers.Factory(DocsRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    company_service = providers.Factory(CompanyService, company_repository=company_repository)
    docs_category_service = providers.Factory(DocsCategoryService, docs_category_repository=docs_category_repository)
    docs_request_service = providers.Factory(DocsRequestService, docs_req_repository=docs_request_repository, user_repository=user_repository)
    docs_service = providers.Factory(DocsService, docs_repository=docs_repository, company_repository=company_repository)