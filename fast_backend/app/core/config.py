import traceback
import logging

from fastapi_mail import ConnectionConfig
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager
import os
from dotenv import load_dotenv
from typing import List
from starlette.templating import Jinja2Templates
from influxdb_client import InfluxDBClient
from app.core.database import Database  # Ensure this path matches your project structure
import sys


# Load environment variables
load_dotenv()

ENV: str = os.getenv("ENV", "dev")

class Configs:
    # Base configuration
    ENV: str = ENV
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    API_V2_STR: str = "/api/v2"
    PROJECT_NAME: str = "MonetX 2.0"
    arbitrary_types_allowed = True
    ENV_DATABASE_MAPPER: dict = {
        "prod": "fca",
        "stage": "stage-fca",
        "dev": "dev-fca",
        "test": "test-fca",
    }
    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql",
        "mysql": "mysql+pymysql",
    }
    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Database configuration
    DB: str = os.getenv("DB", "mysql")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT", "3306")
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "mysql")
    # DATABASE_URL = f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ENV_DATABASE_MAPPER[ENV]}"
    DATABASE_URL = "mysql+pymysql://root:As123456?@updated_atom_db:3306/AtomDB"
    engine = create_engine(DATABASE_URL, query_cache_size=0, pool_size=30, max_overflow=0, pool_pre_ping=True, echo=False, echo_pool=False, pool_recycle=1800, isolation_level="READ COMMITTED")
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    db_session = scoped_session(SessionLocal)
    metadata = MetaData()

    # Pagination configuration
    PAGE = 1
    PAGE_SIZE = 20
    ORDERING = "-id"

    # InfluxDB configuration
    IN_TOKEN: str = "nItzto4Hc22kXuLsawB76lhKPM-wbK1DAQc7uBiFpYUCntoHDE6TC-uGeezzx7S89fyClKv2YXLfDi15Ujhn5A=="
    IN_ORG: str = "monetx"
    IN_BUCKET: str = "monitoring"
    IN_URL: str = "http://updated_influx_db:8086"
    client: InfluxDBClient = InfluxDBClient(url=IN_URL, token=IN_TOKEN)

    templates = Jinja2Templates(directory="/app/templates")

    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_TLS =True
    MAIL_DEBUG = True

    conf = ConnectionConfig(
        MAIL_USERNAME=MAIL_USERNAME,
        MAIL_PASSWORD=MAIL_PASSWORD,
        MAIL_FROM=MAIL_DEFAULT_SENDER,
        MAIL_PORT=MAIL_PORT,
        MAIL_SERVER=MAIL_SERVER,
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )

    @property
    def db(self):
        """Property to get the scoped session for database operations."""
        try:
            return self.db_session()
        except Exception as e:
            self.db_session.remove()
            raise e

    @db.setter
    def db(self, value):
        raise RuntimeError("Operation not allowed.")

    @classmethod
    def init_app(cls, app):
        """
        Initialize the application with configurations for SQLAlchemy.
        This method should be called with your Flask or other framework's app instance.
        """

        @app.teardown_appcontext
        def shutdown_session(exception=None):
            cls.db_session.remove()  # Ensure the session is removed at the end of each request

class Config:
    case_sensitive = True
    orm_mode = True

# Additional Configurations for Testing
class TestConfigs(Configs):
    ENV: str = "test"

configs = Configs()
Base = declarative_base()















if ENV == "prod":
    pass
elif ENV == "stage":
    pass
elif ENV == "test":
    setting = TestConfigs()

# print("logger staterd for sqlalchemy engine:::::::::::::::::::",file=sys.stderr)
# logging.basicConfig(level=logging.DEBUG)
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
# print("logger ended for sqlalchemy engine:::::::::::::::::::::",file=sys.stderr)
