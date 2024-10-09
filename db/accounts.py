from db.db_connection import get_db_connection
from models.plaid import PlaidAccount

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
