from env_settings import postgres_user, postgres_password, postgres_host, postgres_port, postgres_db

_URL = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
