import os
from dotenv import load_dotenv
from pydantic import BaseModel
from plaid import Configuration, ApiClient, Environment
from plaid.api import plaid_api
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

from db.items import get_transactions_cursor, update_transactions_cursor
from models import PlaidAccount

# Load environment variables
load_dotenv()

#Plaid setup
configuration = Configuration(
    host=Environment.Sandbox,
    api_key={
        'clientId': os.getenv("PLAID_CLIENT_ID"),
        'secret': os.getenv("PLAID_SECRET"),
    },
)

plaid_client = ApiClient(configuration)
plaid_api_client = plaid_api.PlaidApi(plaid_client)

class PublicTokenRequest(BaseModel):
    public_token: str


def create_link_token():
     request = LinkTokenCreateRequest(
         user=LinkTokenCreateRequestUser(client_user_id='user-id'),
         client_name="Your App Name",
         products=[Products("transactions")],
         country_codes=[CountryCode('US')],
         language="en",
     )
     response = plaid_api_client.link_token_create(request)
     return response.link_token

def exchange_public_token(request: PublicTokenRequest):
    request = ItemPublicTokenExchangeRequest(public_token=request.public_token)
    response = plaid_api_client.item_public_token_exchange(request)
    access_token = response.access_token
    item_id = response.item_id
    return access_token, item_id

def get_accounts(access_token: str) -> [PlaidAccount]:
    request = AccountsGetRequest(access_token=access_token)
    accounts_response = plaid_api_client.accounts_get(request)
    return accounts_response.accounts

def sync_transactions(item_id: str, access_token: str):
    trans_cursor = get_transactions_cursor(item_id)
    added = []
    modified = []
    removed = []
    has_more = True

    # Iterate through each page of new transaction updates for item
    while has_more:
        request_params = {
            "access_token": access_token,
        }

        if trans_cursor is not None:
            request_params["cursor"] = trans_cursor

        request = TransactionsSyncRequest(**request_params)
        response = plaid_api_client.transactions_sync(request)
        # Add this page of results
        added.extend(response['added'])
        modified.extend(response['modified'])
        removed.extend(response['removed'])
        has_more = response['has_more']
        # Update cursor to the next cursor
        trans_cursor = response['next_cursor']

    # update trans cursor in the DB
    update_transactions_cursor(item_id, trans_cursor)
    return added