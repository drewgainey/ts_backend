# Token and Items operations
from db.db_connection import get_db_connection


def insert_access_token(item_id: str, access_token: str):
    """Insert a new access token into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO items (item_id, access_token) VALUES (?, ?)",
        (item_id, access_token)
    )
    conn.commit()
    conn.close()

def get_transactions_cursor(item_id: str):

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT transactions_cursor FROM items WHERE item_id = ?",
        (item_id,)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return result["transactions_cursor"]
    else:
        return None

def update_transactions_cursor(item_id: str, new_cursor: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE items SET transactions_cursor = ? WHERE item_id = ?",
        (new_cursor, item_id,)
    )
    conn.commit()
    conn.close()