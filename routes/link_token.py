import sqlite3

from fastapi import APIRouter, HTTPException

from db import insert_accounts, insert_access_token, insert_transaction_data, insert_institution
from models import PublicTokenRequest
from util.plaid_client import create_link_token, exchange_public_token, get_accounts, sync_transactions, get_item_details, get_institution

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

        # Get institution information for linked item
        item = get_item_details(access_token)
        institution = get_institution(institution_id=item.institution_id)
        db_institution_id = insert_institution(plaid_institution_id=item.institution_id, institution_name=institution.institution.name)
        # Get account(s) information
        accounts = get_accounts(access_token)
        insert_accounts(item_id=item_id, accounts=accounts, institution_id=db_institution_id)
        # Get transactions up to date
        added = sync_transactions(item_id=item_id, access_token=access_token)
        insert_transaction_data(added)
        return {"message": "Token exchanged and transactions synced successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Database Error")
    except Exception as e:
        print(f'Error:{e}')
        raise HTTPException(status_code=400, detail=f"Error exchanging public token: {str(e)}")
