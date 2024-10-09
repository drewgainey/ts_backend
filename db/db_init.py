from .db_connection import get_db_connection

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
                description TEXT,
                merchant_id INTEGER,
                currency TEXT NOT NULL,
                pending BOOLEAN,
                gl_account_id INTEGER,
                status_id INTEGER,
                FOREIGN KEY(account_id) REFERENCES accounts(account_id),
                FOREIGN KEY(merchant_id) REFERENCES merchants(id),
                FOREIGN KEY(gl_account_id) REFERENCES gl_accounts(id),
                FOREIGN KEY(status_id) REFERENCES transactions_status(id)
            )
        ''')
    # Create transactions status table
    cursor.execute('''
             CREATE TABLE IF NOT EXISTS transactions_status (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 status TEXT NOT NULL UNIQUE
             )
         ''')
    cursor.execute('''
         INSERT OR IGNORE INTO 
            transactions_status (status) 
        values 
        ('unclassified'), 
        ('unmatched'), 
        ('matched')
     ''')

    # Create merchants table
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS merchants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                merchant_name TEXT NOT NULL UNIQUE,
                logo_url TEXT
            )
        ''')
    cursor.execute('''
        INSERT OR IGNORE INTO merchants (merchant_name) values ('No Merchant Available')
    ''')

    # Create GL Accounts table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS gl_accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    gl_account_number TEXT NOT NULL UNIQUE,
                    gl_account_name TEXT NOT NULL UNIQUE
                )
            ''')

    cursor.execute('''
        INSERT OR IGNORE INTO gl_accounts (gl_account_number, gl_account_name) 
        values ('1000', 'Cash'),
        ('2000', 'Liabilities'),  
        ('3000', 'Equity'),
        ('4000', 'Revenue')  
    ''')
    conn.commit()
    conn.close()
