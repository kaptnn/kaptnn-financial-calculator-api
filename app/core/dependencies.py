import jwt
from uuid import UUID
from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import ValidationError
from app.core.config import configs
from app.core.container import Container
from app.schema.user_schema import FindUserByOptionsResponse, User
from app.services.user_service import UserService

@inject
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    service: UserService = Depends(Provide[Container.user_service])
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            configs.JWT_SECRET_KEY,
            algorithms=['HS256']
        )
        user_id = UUID(payload.get("sub", ""))
    except Exception:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token format"
        )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
            
    response: FindUserByOptionsResponse = service.get_user_by_options("id", user_id)
    current_user = response.result
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return current_user