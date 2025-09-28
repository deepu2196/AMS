from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import Dict
from app.core.config import DBSettings

# Load config params
db_settings = DBSettings.from_env()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = db_settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    """
    Converts given password to hashed password.

    Args:
        password (str): Password to hash

    Returns:
        str: Hashed password
    """
    if not isinstance(password, str):
        raise TypeError("Password must be a string")
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """
    Verifies whether password and hashed password are same.
    """
    return pwd_context.verify(password, hashed)

def create_access_token(data: Dict, expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    Creates access token 

    Args:
        data (Dict): user details { user_id, is_admin }
        expires_minutes (int): Token expire time in minutes

    Returns:
        str: JWT Token
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    """
    Decodes given access token and verifies a JWT string's signature.

    Args:
        token (str): User token

    Returns:
        dict
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")