import os
from dotenv import load_dotenv

load_dotenv()

postgres_port = os.getenv("POSTGRES_PORT")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
secret_key = os.getenv("SECRET_KEY_FOR_CSRF")
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_db = os.getenv("REDIS_DB")
