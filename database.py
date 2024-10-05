import sqlite3

from models import PlaidAccount, PlaidTransaction

# Define the path for the SQLite database
DB_PATH = "treasury.db"

def init_db():
    """Initialize the SQLite database and create the required tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
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

def get_db_connection():
    """Create a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise Exception("Database connection error")

# Token and Items operations
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

# Account information operations
def insert_accounts(item_id: str, accounts: [PlaidAccount]):
    """Insert a new account into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    account_data = [(
        account.account_id,
        item_id,
        account.name,
        account.official_name if account.official_name is not None else account.name,
        str(account.type),
        str(account.subtype),
        account.mask,
        account.balances.available if account.balances.available is not None else 0.0,
        account.balances.current if account.balances.current is not None else 0.0,
        account.balances.limit if account.balances.limit is not None else 0.0,
        str(account.balances.iso_currency_code)
        ) for account  in accounts]
   
    cursor.executemany(
        '''
        INSERT OR IGNORE INTO accounts 
        (account_id, item_id, account_name, account_official_name, account_type, account_subtype, mask, balance_available, balance_current, balance_limit, currency) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        account_data
    )
    conn.commit()
    conn.close()


# Transacations
def insert_transaction_data(transactions: [PlaidTransaction]):
    conn = get_db_connection()
    cursor = conn.cursor()
    """Insert any new merchants into the merchants table and get merchant id's"""
    unique_merchants = {trans.name for trans in transactions}
    unique_merchants_tuple = tuple(unique_merchants)

    merchant_query = 'SELECT id, merchant_name FROM merchants WHERE merchant_name IN ({})'.format(
        ','.join('?' * len(unique_merchants_tuple)))
    cursor.execute(merchant_query, unique_merchants_tuple)
    merchant_dict = {row['merchant_name']: row['id'] for row in cursor.fetchall()}

    missing_merchants = unique_merchants - set(merchant_dict.keys())
    for name in missing_merchants:
        cursor.execute('INSERT INTO merchants (merchant_name) VALUES (?)', (name,))
    conn.commit()

    if missing_merchants:
        query = 'SELECT id, merchant_name FROM merchants WHERE merchant_name IN ({})'.format(
            ','.join('?' * len(missing_merchants)))
        cursor.execute(query, tuple(missing_merchants))

        # Update the merchant_dict with the new merchant IDs
        merchant_dict.update({row['merchant_name']: row['id'] for row in cursor.fetchall()})
    """Inset transactions"""
    transactions_data = [(
        trans.transaction_id,
        trans.account_id,
        trans.amount,
        trans.date,
        merchant_dict[trans.name],
        trans.iso_currency_code,
        trans.pending,
    ) for trans in transactions]

    cursor.executemany(
        '''
        INSERT OR IGNORE INTO transactions 
        (transaction_id, account_id, amount, date, merchant_id, currency, pending) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''',
        transactions_data
    )

    conn.commit()
    conn.close()

def get_transaction_details():
    conn = get_db_connection()
    cursor = conn.cursor()
    """Get all transactions on join account name and merchant name"""
    cursor.execute(
        """
        select
                t.transaction_id transaction_id,
                a.account_name account_name,
                a.account_official_name account_official_name,
                t.amount amount,
                t.date date,
                m.merchant_name merchant_name,
                t.currency currency,
                t.pending pending,
                g.gl_account_number gl_account_number,
                g.gl_account_name gl_account_name
        from transactions t
            inner join accounts a on t.account_id = a.account_id
            left join merchants m on m.id = t.merchant_id
            left join gl_accounts g on g.id = t.gl_account_id
        """)
    result = cursor.fetchall()

    transactions = [
        {
            "transaction_id": row["transaction_id"],
            "account_name": row["account_name"],
            "account_official_name": row["account_official_name"],
            "amount": row["amount"],
            "date": row["date"],
            "merchant_name": row["merchant_name"],
            "currency": row["currency"],
            "pending": row["pending"],
            "gl_account_number": row["gl_account_number"],
            "gl_account_name": row["gl_account_name"]
        }
        for row in result
    ]

    return transactions
