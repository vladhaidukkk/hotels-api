import os

from dotenv import load_dotenv

load_dotenv()


DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_USER = os.environ["DB_USER"]
DB_PASS = os.environ["DB_PASS"]
DB_NAME = os.environ["DB_NAME"]


def create_db_url(driver: str):
    return f"postgresql+{driver}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


SYNC_DB_URL = create_db_url("psycopg")
ASYNC_DB_URL = create_db_url("asyncpg")
