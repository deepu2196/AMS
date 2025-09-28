from pydantic import BaseModel, EmailStr

# Input Models
class UserLogin(BaseModel):
    """
    User Login class represents structure of User for login to AMS

    Attributes:
        username (str): username of the user
        password (str): password of the user
    """
    username: str
    password: str

    
class BaseUser(BaseModel):
    """
    Base User class represents fundamental structure of the user in AMS

    Attributes:
        username (str): username of the user
        email (EmailStr): email of the user
        is_admin (bool): admin privilege of the user
        flat_no (int): flat number of the user
    """
    username: str
    email: EmailStr
    is_admin: bool
    flat_no: int


class UserCreate(BaseUser):
    """
    User Create class represents structure of User for creating new user in AMS

    Attributes:
        password (str): password of the user
    """
    password: str

class User(BaseUser):
    """
    User class represents structure of user used in AMS

    Attributes:
        password (str): password of the user
    """
    id: int

# Output Models
class UserCreatedResponse(BaseModel):
    id: int

class GetUserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
