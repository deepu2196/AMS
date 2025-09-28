from mysql.connector import pooling, errorcode
import mysql.connector
from typing import Optional, List, Dict, Any
from app.core.config import DBSettings
from app.entity.user import UserCreate
from app.utils import Singleton, SingletonLogger
# from entity.expenses import *

logger = SingletonLogger()


class Database(metaclass=Singleton):

    def __init__(self, db_settings: DBSettings):
        logger.log("Connecting to Database")
        self.db_settings = db_settings
        self._conn = None
        self._pool = self._create_pool()
        

    # def connect(self):
    #     self._pool = self._create_pool()

    def _create_pool(self) -> pooling.PooledMySQLConnection:
        logger.log("Getting pooled connection")
        return pooling.MySQLConnectionPool(
            pool_name=self.db_settings.DB_POOL_NAME,
            pool_size=self.db_settings.DB_POOL_SIZE,
            host=self.db_settings.DB_HOST,
            port=self.db_settings.DB_PORT,
            user=self.db_settings.DB_USER,
            password=self.db_settings.DB_PASSWORD,
            database=self.db_settings.DB_NAME,
            charset="utf8mb4",
            autocommit=False,
            use_unicode=True
        )
    
    def get_cursor(self):
        if self._conn is None:
            #Connect for the first time
            self._conn = self._pool.get_connection()
        try:
            cursor = self._conn.cursor()
        except mysql.connector.Error as err:
            logger.error(err)

    #------------------USERS------------------
    def create_user(self, user_details: UserCreate) -> int:
        logger.log(f"Creating new user - {user_details.username}.")
        with self.get_cursor as cursor:
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin, flat_no) VALUES (%s, %s, %s, %s, %s)",
                (user_details.username, user_details.email, user_details.password, user_details.is_admin, user_details.flat_no),
            )
            cursor.connection.commit()
            logger.log(f"User {user_details.username} created.")
            return cursor.lastrowid

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        logger.log(f"Retrieving user details of {username}.")
        with self.get_cursor as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cursor.fetchone()

# def db_connection():
#     #Connection to mysql DB
#     connection_sql = mysql.connector.connect(
#         host='10.0.0.210',   
#         user='admin',          
#         password='Ams@2196',      
#         database='test_db',             
#         port=3306                            
#     )
#     return connection_sql

# def create_users():
#     conn = db_connection()
#     cursor = conn.cursor()

#     insert_stmt = """
#         INSERT INTO users (name, email, password_hash, is_admin, created_at)
#         VALUES (%s, %s, %s, %s, NOW())
#     """
#     data = ('test', 'test@exp.com', 'test12##', 1)
#     cursor.execute(insert_stmt, data)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return "successfully inserted"

# def insert_expense(expense: baseexpenses):
#     print("getting connection")
#     conn = db_connection()
#     cursor = conn.cursor()

#     logger.info("connection established")

#     insert_stmt = """
#         INSERT INTO expenses (title, description, amount, date, user_id, created_at)
#         VALUES (%s, %s, %s, %s)
#     """
#     data = (expense.title, expense.description, expense.amount, date.today(), 1, datetime.now())
#     cursor.execute(insert_stmt, data)
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return "successfully inserted"

# def expenses_details(expense: baseexpenses):
#     conn = db_connection()
#     cursor = conn.cursor()
#     select_stmt="""
#         Select * from expenses where expenses.user_id=%s
#     """
#     data=(expense.user_id)
#     cursor.execute(select_stmt,data)
#     expense_record=cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return expense_record
