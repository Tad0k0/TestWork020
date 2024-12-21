import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

db_drivers = {"postgresql": "asyncpg"}
db_sync_drivers = {"postgresql": "psycopg"} #use for alembic

# Load environment
load_dotenv(dotenv_path="./.env")

class Settings(BaseSettings):
    log_level: str = os.getenv('LOG_LEVEL')
    api_key: str = os.getenv('API_KEY')
    app_host: str = os.getenv('APP_HOST')
    app_port: int = os.getenv('APP_PORT')
    db_engine: str = os.environ.get("DB_ENGINE")
    db_sync_driver: str = db_sync_drivers[os.environ.get("DB_ENGINE")]
    db_driver: str = db_drivers[os.environ.get("DB_ENGINE")]
    db_server: str = os.environ.get("DB_SERVER")
    db_port: int = os.environ.get("DB_PORT")
    db_name: str = os.environ.get("DB_NAME")
    db_user: str = os.environ.get("DB_USER")
    db_password: str = os.environ.get("DB_PASSWORD")
    db_url: str = f"{db_engine}+{db_driver}://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    db_sync_url: str = f"{db_engine}+{db_sync_driver}://{db_user}:{db_password}@{db_server}:{db_port}/{db_name}"
    redis_url: str = f"redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}"


settings = Settings()

