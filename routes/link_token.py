import sqlite3

from fastapi import APIRouter, HTTPException

from db.accounts import insert_accounts
from db.items import insert_access_token
from db.transactions import insert_transaction_data
from models.api import PublicTokenRequest
from util.plaid_client import create_link_token, exchange_public_token, get_accounts, sync_transactions

router = APIRouter(prefix='/link_token', tags=['link_token'])

@router.post("/create")
async def create_link_token_api():
    try:
        link_token = create_link_token()
        return {"link_token": link_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating link token: {str(e)}")

@router.post("/exchange")
async def exchange_public_token_api(request: PublicTokenRequest):
    """Endpoint to exchange a public token for an access token and store it in the database."""
    try:
        access_token, item_id = exchange_public_token(request)
        insert_access_token(item_id, access_token)

        # Get account(s) information
        accounts = get_accounts(access_token)
        insert_accounts(item_id=item_id, accounts=accounts)
        # Get transactions up to date
        added = sync_transactions(item_id=item_id, access_token=access_token)
        insert_transaction_data(added)
        return {"message": "Token exchanged and transactions synced successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Database Error")
    except Exception as e:
        print(f'Error:{e}')
        raise HTTPException(status_code=400, detail=f"Error exchanging public token: {str(e)}")
