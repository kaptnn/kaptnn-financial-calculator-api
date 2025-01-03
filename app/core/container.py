from dependency_injector import containers, providers
from app.core.config import configs
from app.core.database import Database
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.routes.endpoints.auth",
            "app.routes.endpoints.user",
            "app.routes.endpoints.calculator",
            "app.routes.endpoints.goal_seeking",
            "app.core.dependencies",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DB_URI)

    user_repository = providers.Factory(UserRepository, session_factory=db.provided.session)

    user_service = providers.Factory(UserService, user_repository=user_repository)
    auth_service = providers.Factory(AuthService, user_repository=user_repository)