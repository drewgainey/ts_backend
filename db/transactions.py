from db.db_connection import get_db_connection
from models import PlaidTransaction

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
