from .db_connection import get_db_connection
from .schemas import ALL_SCHEMAS

def init_db():
    """Initialize the SQLite database and create the required tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    for schema in ALL_SCHEMAS:
         cursor.execute(schema)

    conn.commit()
    conn.close()
