from db.db_connection import get_db_connection

def get_all_fields():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gl_accounts")
    result = cursor.fetchall()
    return result