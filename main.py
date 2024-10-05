import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import List
from database import init_db, insert_access_token, insert_accounts, insert_transaction_data, get_transaction_details
from plaid_client import create_link_token, exchange_public_token, get_accounts, sync_transactions
from models import PublicTokenRequest, TransactionDetailResponse

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize the database when the app starts
init_db()

@app.post("/create_link_token")
async def create_link_token_api():
    """Endpoint to create a Plaid link token."""
    try:
        link_token = create_link_token()
        return {"link_token": link_token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating link token: {str(e)}")

@app.post("/exchange_public_token")
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
        print(e)
        raise HTTPException(status_code=400, detail=f"Error exchanging public token: {str(e)}")

@app.get("/account_details", response_model=List[TransactionDetailResponse])
def api_get_accounts_with_transactions():
    """API route to fetch all accounts with their associated transactions."""
    try:
        accounts_with_transactions = get_transaction_details()
        return accounts_with_transactions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accounts and transactions: {e}")