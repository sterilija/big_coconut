from os import getenv
from dotenv import load_dotenv

load_dotenv()


class DBCreds:
    USERNAME = getenv("DB_USERNAME")
    PASSWORD = getenv("DB_PASSWORD")
    HOST = getenv("DB_HOST")
    PORT = getenv("DB_PORT")
    TABLE = getenv("DB_TABLE")
