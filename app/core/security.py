from fastapi import HTTPException
import jwt
from datetime import datetime, timedelta
from app.core.config import configs
from app.schema.auth_schema import Token

def create_access_token(data: dict):
    to_encode = data.copy()
    if configs.JWT_ACCESS_TOKEN_EXP:
        expire = datetime.now() + timedelta(days=int(configs.JWT_ACCESS_TOKEN_EXP[:-1]))
    else:
        expire = datetime.now() + timedelta(hours=1)
    to_encode.update({"exp": expire, "membership_status": data.get("membership_status", "default")})

    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    if configs.JWT_REFRESH_TOKEN_EXP:
        expire = datetime.now() + timedelta(days=int(configs.JWT_REFRESH_TOKEN_EXP[:-1]))
    else:
        expire = datetime.now() + timedelta(days=7)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, configs.KEY)
    return encoded_jwt

def create_new_access_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, configs.KEY, algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_payload = {
        "sub": payload.get("sub"),
    }

    return Token(
        token_type="Bearer",
        access_token  = create_access_token(new_payload),
        refresh_token = create_refresh_token(new_payload),
    )
