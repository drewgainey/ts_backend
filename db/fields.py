from .db_connection import get_db_connection

def get_all_fields():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gl_accounts")
    gl_accounts = cursor.fetchall()

    cursor.execute("SELECT * FROM accounting_entities")
    accounting_entities = cursor.fetchall()

    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()

    result = {
        'gl_accounts': gl_accounts,
        'accounting_entities': accounting_entities,
        'departments': departments
    }
    return result