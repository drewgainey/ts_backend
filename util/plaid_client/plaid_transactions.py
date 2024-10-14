from plaid.model.transactions_sync_request import TransactionsSyncRequest
from .plaid_client import plaid_api_client
from db import get_transactions_cursor, update_transactions_cursor

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