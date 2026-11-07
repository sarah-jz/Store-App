
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB = os.getenv("MYSQL_DB", "project_computer")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is missing from .env")

    if MYSQL_PASSWORD is None:
        raise RuntimeError("MYSQL_PASSWORD is missing from .env")
