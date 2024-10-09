from typing import List

from fastapi import APIRouter, HTTPException

from db import get_transaction_details
from models import TransactionDetailResponse

router = APIRouter(prefix='/accounts', tags=['accounts'])

@router.get("/details", response_model=List[TransactionDetailResponse])
def api_get_accounts_with_transactions():
    """API route to fetch all accounts with their associated transactions."""
    try:
        accounts_with_transactions = get_transaction_details()
        return accounts_with_transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accounts and transactions: {e}")