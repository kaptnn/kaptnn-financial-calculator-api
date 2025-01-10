import jwt
from datetime import datetime, timedelta

from app.core.config import configs

def create_access_token(data: dict):
    to_encode = data.copy()
    if configs.JWT_ACCESS_TOKEN_EXP:
        expire = datetime.now() + timedelta(days=int(configs.JWT_ACCESS_TOKEN_EXP[:-1]))
    else:
        expire = datetime.now() + timedelta(days=1)
    to_encode.update({"exp": expire, "membership_status": data.get("membership_status", "default")})

    encoded_jwt = jwt.encode(to_encode, configs.JWT_SECRET_KEY, algorithm="HS256")
    
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    if configs.JWT_REFRESH_TOKEN_EXP:
        expire = datetime.now() + timedelta(days=int(configs.JWT_REFRESH_TOKEN_EXP[:-1]))
    else:
        expire = datetime.now() + timedelta(days=30)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, configs.KEY)
    return encoded_jwt