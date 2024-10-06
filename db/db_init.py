import sqlite3

from db.db_connection import get_db_connection

def init_db():
    """Initialize the SQLite database and create the required tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create access tokens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT NOT NULL,
            access_token TEXT UNIQUE NOT NULL,
            transactions_cursor TEXT UNIQUE
        )
    ''')

    # Create accounts table if it doesn't exist
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS accounts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              account_id TEXT NOT NULL,
              item_id TEXT NOT NULL,
              account_name TEXT NOT NULL,
              account_official_name TEXT NOT NULL,
              account_type TEXT NOT NULL,
              account_subtype TEXT NOT NULL,
              mask INTEGER,
              balance_available REAL,
              balance_current REAL,
              balance_limit REAL,
              currency TEXT NOT NULL
          )
      ''')

    # Create transactions table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT NOT NULL,
                account_id TEXT NOT NULL,
                amount REAL,
                date DATE,
                merchant_id INTEGER,
                currency TEXT NOT NULL,
                pending BOOLEAN,
                gl_account_id INTEGER,
                FOREIGN KEY(account_id) REFERENCES accounts(account_id),
                FOREIGN KEY(merchant_id) REFERENCES merchants(id),
                FOREIGN KEY(gl_account_id) REFERENCES gl_accounts(id)
            )
        ''')

    # Create merchants table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS merchants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merchant_name TEXT NOT NULL UNIQUE
            )
        ''')

    # Create GL Accounts table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS gl_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gl_account_number TEXT NOT NULL UNIQUE,
                    gl_account_name TEXT NOT NULL UNIQUE
                )
            ''')

    conn.commit()
    conn.close()
