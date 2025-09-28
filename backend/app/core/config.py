import os
from app.utils import SingletonLogger
logger = SingletonLogger()

class DBSettings:
    def __init__(self,
                 db_host: str,
                 db_port: int,
                 db_name: str,
                 db_user: str,
                 db_password: str,
                 db_pool_name: str,
                 db_pool_size: int,
                 secret_key: str):
        self.DB_HOST = db_host
        self.DB_PORT = db_port
        self.DB_NAME = db_name
        self.DB_USER = db_user
        self.DB_PASSWORD = db_password
        self.DB_POOL_NAME = db_pool_name
        self.DB_POOL_SIZE = db_pool_size
        self.SECRET_KEY = secret_key

    @classmethod
    def from_env(cls):
        """Load settings from environment variables"""
        return cls(
            db_host=os.environ.get("DB_HOST", "10.0.0.210"),
            db_port=int(os.environ.get("DB_PORT", 3306)),
            db_name=os.environ.get("DB_NAME", "test_db"),
            db_user=os.environ.get("DB_USER", "admin"),
            db_password=os.environ.get("DB_PASSWORD", ""),
            db_pool_name=os.environ.get("DB_POOL_NAME", "ams_pool"),
            db_pool_size=int(os.environ.get("DB_POOL_SIZE", 2)),
            secret_key=os.environ.get("SECRET_KEY", "changeme123")
        )

    @classmethod
    def from_dict(cls, d: dict):
        """Load settings from a dictionary"""
        return cls(
            db_host=d.get("DB_HOST", "127.0.0.1"),
            db_port=int(d.get("DB_PORT", 3306)),
            db_name=d.get("DB_NAME", "ams_db"),
            db_user=d.get("DB_USER", "ams_user"),
            db_password=d.get("DB_PASSWORD", ""),
            db_pool_name=d.get("DB_POOL_NAME", "ams_pool"),
            db_pool_size=int(d.get("DB_POOL_SIZE", 2)),
            secret_key=d.get("SECRET_KEY", "changeme123")
        )