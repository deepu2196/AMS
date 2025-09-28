from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import DBSettings
from app.core.auth import hash_password, verify_password, create_access_token, get_current_user
from app.db import Database
from app.entity.user import UserCreate, UserLogin, UserCreatedResponse, TokenResponse
from app.utils import SingletonLogger
from app.db import *
from entity.expenses import baseExpense, expenseCreatedResponse

logger = SingletonLogger()

def create_app() -> FastAPI:

    #Connecting to DB
    db_settings = DBSettings.from_env()
    db_connection = Database(db_settings)

    #constants
    AUTHENTICATION_TAG = "Authentication"
    EXPENSES_TAG = "Expenses"
    USERS_TAG = "Users"

    tags_metadata = [
        {
            "name": AUTHENTICATION_TAG,
            "description": "Operations related to user authentication like register and login",
        },
        {
            "name": EXPENSES_TAG,
            "description": "Operations related to expenses, reports, and corpus",
        },
        {
            "name": USERS_TAG,
            "description": "User management and admin-related operations",
        },
    ]
    
    # Create FastAPI application
    app = FastAPI(
        title="Apartment Management System",
        description="REST API Documentation",
        version="0.0.1",
        openapi_tags=tags_metadata,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # Define the API Endpoints

    @app.get("/")
    def read_root():
        return {"msg": "Apartment Management System"}
    
    # Authentication API

    @app.post(
        "/register",
        response_model=UserCreatedResponse,
        tags=[AUTHENTICATION_TAG],
        status_code=status.HTTP_201_CREATED
    )
    def register(user: UserCreate) -> UserCreatedResponse:
        if db_connection.get_user_by_username(user.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed = hash_password(user.password)
        user.password = hashed
        user_id = db_connection.create_user(user)
        return {"id": user_id}

    @app.post(
        "/login",
        response_model=TokenResponse,
        tags=[AUTHENTICATION_TAG],
        responses={400: {"description": "Bad Request: incorrect credentials"}}
    )
    async def login(user: UserLogin) -> TokenResponse:
        db_user = db_connection.get_user_by_username(user.username)
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"user_id": db_user["id"], "is_admin": db_user["is_admin"]})
        return {"access_token": token, "token_type": "bearer"}
    
    # Expenses API
    
    @app.post(
        "/expenses",
        response_model=expenseCreatedResponse,
        ags=[EXPENSES_TAG]
    )
    def create_expense(expense: baseExpense, current_user: dict = Depends(get_current_user)) -> expenseCreatedResponse:
        user_id = current_user["id"]
        return db_connection.create_expense(expense, user_id)

    return app

# @app.get("/expenses")
# def get_expenses(expense:baseexpenses):
#     print("get expense endpoint called")
#     return expenses_details(expense)