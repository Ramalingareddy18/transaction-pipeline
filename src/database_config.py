import os
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv

    from project_paths import PROJECT_ROOT

    load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
except Exception:
    # Ignore if dotenv is unavailable or the project path isn't importable yet.
    pass


def get_db_settings(database_name=None):
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "postgres")
    db_name = database_name or os.getenv("DB_NAME", "transaction_pipeline_db")
    db_password = os.getenv("DB_PASSWORD")

    if not db_password:
        raise RuntimeError(
            "DB_PASSWORD environment variable is not set. "
            "Create a .env file in the project root with DB_PASSWORD."
        )

    return {
        "host": db_host,
        "port": db_port,
        "user": db_user,
        "password": db_password,
        "name": db_name,
    }


def build_database_url(database_name=None):
    settings = get_db_settings(database_name)
    password = quote_plus(settings["password"])
    return (
        f"postgresql+psycopg2://{settings['user']}:{password}"
        f"@{settings['host']}:{settings['port']}/{settings['name']}"
    )


def build_admin_url():
    settings = get_db_settings()
    password = quote_plus(settings["password"])
    return (
        f"postgresql+psycopg2://{settings['user']}:{password}"
        f"@{settings['host']}:{settings['port']}/postgres"
    )
