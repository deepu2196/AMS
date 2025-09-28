from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from typing import Dict
from app.db import Database
from app.core.config import DBSettings
from app.entity.user import GetUserResponse
from app.utils import SingletonLogger

logger = SingletonLogger()

# Load config params
db_settings = DBSettings.from_env()
db_connection = Database(db_settings)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = db_settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

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

def get_current_user(token: str = Depends(oauth2_scheme)) -> GetUserResponse:
        """
        Gets current user based on the token provided.

        Args:
            token (str): User token

        Returns:
            dict
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            logger.log("Retrieving Payload.")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.log(f"Payload retrieved: {payload}.")
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = db_connection.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user