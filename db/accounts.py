from .db_connection import get_db_connection
from models import PlaidAccount

def insert_institution(plaid_institution_id: str, institution_name: str) -> int:
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the institution already exists
    cursor.execute('''
        SELECT id FROM institutions WHERE plaid_institution_id = ?
    ''', (plaid_institution_id,))
    result = cursor.fetchone()

    # If the institution exists, return the id
    if result:
        institution_id = result[0]
    else:
        # Otherwise, insert the new institution and get the id
        cursor.execute('''
            INSERT INTO institutions (plaid_institution_id, institution_name)
            VALUES (?, ?)
        ''', (plaid_institution_id, institution_name))
        institution_id = cursor.lastrowid
        conn.commit()

    # Close the connection and return the institution ID
    conn.close()
    return institution_id

# Account information operations
def insert_accounts(item_id: str, accounts: [PlaidAccount], institution_id: int):
    """Insert a new account into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    account_data = [(
        account.account_id,
        institution_id,
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
        (account_id, institution_id, item_id, account_name, account_official_name, account_type, account_subtype, mask, balance_available, balance_current, balance_limit, currency) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        account_data
    )
    conn.commit()
    conn.close()

def get_bank_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            a.id account_id,
            i.institution_name institution_name,
            a.account_name account_name,
            a.account_official_name account_official_name,
            a.account_type account_type,
            a.account_subtype account_subtype,
            a.mask mask,
            a.balance_available balance_available,
            a.balance_current balance_current
        FROM accounts a
        LEFT JOIN institutions i on a.institution_id = i.id
    ''')
    result = cursor.fetchall()

    accounts = [
        {
            "account_id": row["account_id"],
            "institution_name": row["institution_name"],
            "account_name": row["account_name"],
            "account_official_name": row["account_official_name"],
            "account_type": row["account_type"],
            "account_subtype": row["account_subtype"],
            "mask": row["mask"],
            "balance_available": row["balance_available"],
            "balance_current": row["balance_current"]
        }
        for row in result
    ]

    conn.close()
    return {"accounts" : accounts}