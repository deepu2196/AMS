from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import DBSettings
from app.core.auth import hash_password, verify_password, create_access_token
from app.db import Database
from app.entity.user import UserCreate, UserLogin
from app.db import *
# from entity.expenses import *


def create_app() -> FastAPI:

    #Connecting to DB
    db_settings = DBSettings.from_env()
    db_connection = Database(db_settings)
    

    app = FastAPI(
        title="Apartment Management System",
        description="REST API Documentation",
        version="0.0.1",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    # @app.on_event("startup")
    # def on_startup():
    #     pass
    #     # db_connection.connect()  # connect once when app starts

    # # Shutdown event
    # @app.on_event("shutdown")
    # def on_shutdown():
    #     if db_connection.conn:
    #         db_connection.conn.close()

    @app.get("/")
    def read_root():
        print("root endpoint called")
        return {"msg": "Apartment Management System"}

    @app.post("/register")
    def register(user: UserCreate):
        if db_connection.get_user_by_username(user.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        hashed = hash_password(user.password)
        user_id = db_connection.create_user(user)
        return {"id": user_id}

    @app.post("/login")
    async def login(user: UserLogin):
        db_user = await db_connection.get_user_by_username(user.username)
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = create_access_token({"user_id": db_user["id"], "is_admin": db_user["is_admin"]})
        return {"access_token": token, "token_type": "bearer"}
    
    return app


# @app.post("/expenses")
# def create_expense(expense:baseexpenses):
#     print("post expense endpoint called")
#     return insert_expense(expense)

# @app.get("/expenses")
# def get_expenses(expense:baseexpenses):
#     print("get expense endpoint called")
#     return expenses_details(expense)