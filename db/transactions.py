from .db_connection import get_db_connection
from models import PlaidTransaction


def insert_transaction_data(transactions: [PlaidTransaction]):
    conn = get_db_connection()
    cursor = conn.cursor()

    """Insert any new merchants into the merchants table and get merchant IDs"""
    unique_merchants = {(trans.merchant_name, trans.logo_url) for trans in transactions if
                        trans.merchant_name is not None}
    unique_merchants_tuple = tuple(merchant for merchant in unique_merchants)

    # Modify the merchant query to search for both merchant name and logo URL
    merchant_query = 'SELECT id, merchant_name FROM merchants WHERE merchant_name IN ({})'.format(
        ','.join('?' * len([name for name, logo in unique_merchants_tuple])))

    merchant_names = [name for name, logo in unique_merchants_tuple]  # Extract just the names for query
    cursor.execute(merchant_query, tuple(merchant_names))
    merchant_dict = {row['merchant_name']: row['id'] for row in cursor.fetchall()}
    missing_merchants = set(merchant_names) - set(merchant_dict.keys())

    # Insert new merchants, with logo_url if available
    for name, logo_url in unique_merchants:
        if name in missing_merchants:
            cursor.execute(
                '''
                INSERT INTO merchants (merchant_name, logo_url) 
                VALUES (?, ?)
                ''',
                (name, logo_url)  # Insert logo_url along with merchant name
            )
    conn.commit()

    # Update merchant_dict with new merchant IDs
    if missing_merchants:
        query = 'SELECT id, merchant_name FROM merchants WHERE merchant_name IN ({})'.format(
            ','.join('?' * len(missing_merchants)))
        cursor.execute(query, tuple(missing_merchants))

        # Update the merchant_dict with the new merchant IDs
        merchant_dict.update({row['merchant_name']: row['id'] for row in cursor.fetchall()})

    """Insert transactions"""
    transactions_data = [(
        trans.transaction_id,
        trans.account_id,
        trans.amount,
        trans.date,
        trans.name,
        merchant_dict.get(trans.merchant_name, 1),
        trans.iso_currency_code,
        trans.pending
    ) for trans in transactions]

    cursor.executemany(
        '''
        INSERT OR IGNORE INTO transactions 
        (transaction_id, account_id, amount, date, description, merchant_id, currency, pending) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
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
                t.description description,
                m.merchant_name merchant_name,
                m.logo_url logo_url,
                t.currency currency,
                t.pending pending
        from transactions t
            inner join accounts a on t.account_id = a.account_id
            left join merchants m on m.id = t.merchant_id
        """)
    result = cursor.fetchall()

    transactions = [
        {
            "transaction_id": row["transaction_id"],
            "account_name": row["account_name"],
            "account_official_name": row["account_official_name"],
            "amount": row["amount"],
            "date": row["date"],
            "description": row["description"],
            "merchant_name": row["merchant_name"],
            "logo_url": row["logo_url"],
            "currency": row["currency"],
            "pending": row["pending"],
        }
        for row in result
    ]

    return transactions
