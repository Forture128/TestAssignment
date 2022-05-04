import os


def form_connection_string(db_name: str, port=5432):
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    if user is None or password is None:
        raise RuntimeError("Database user, pass not set in environment")
    print(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


class Config:
    ENV = "local"
    SQLALCHEMY_DB_URI = form_connection_string("zymo_db")

    # REDIS_HOST = "localhost"
    # REDIS_PORT = 6379
    # JSON_DATA = "covid-stats.json"
