from typing import List

from fastapi import APIRouter, HTTPException

from db import get_transaction_details, get_bank_accounts
from models import AccountDetailResponse

router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.get(path='')
def api_get_account():
    accounts = get_bank_accounts()
    return accounts
@router.get("/details", response_model=List[AccountDetailResponse])
def api_get_accounts_with_transactions():
    """API route to fetch all accounts with their associated transactions."""
    try:
        accounts_with_transactions = get_transaction_details()
        return accounts_with_transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accounts and transactions: {e}")