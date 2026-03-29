from psycopg import connect
from psycopg.rows import dict_row

from app.core.settings import get_settings


def get_db_connection():
    settings = get_settings()

    if not settings.supabase_db_url:
        raise ValueError("SUPABASE_DB_URL is not configured.")

    return connect(settings.supabase_db_url, row_factory=dict_row)


def check_database_connection() -> dict[str, str]:
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("select current_database() as database_name;")
            row = cursor.fetchone()

    return {
        "database_name": row["database_name"],
        "status": "ok",
    }

