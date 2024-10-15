from models import TransactionMatch
from typing import List
from .db_connection import get_db_connection

def match_transactions(matches: List[TransactionMatch]):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executemany('''
        INSERT INTO transaction_matches (erp_transaction_id, transaction_id, matched_amount)
        VALUES (?, ?, ?)
    ''', matches)

    conn.commit()
    conn.close()