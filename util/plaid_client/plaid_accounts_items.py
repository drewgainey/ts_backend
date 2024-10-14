from plaid.model.country_code import CountryCode
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest

from models import PlaidAccount
from .plaid_client import plaid_api_client
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest

def get_item_details(access_token: str):
    request = ItemGetRequest(access_token)
    response = plaid_api_client.item_get(request)
    return response.item

def get_accounts(access_token: str) -> [PlaidAccount]:
    request = AccountsGetRequest(access_token=access_token)
    accounts_response = plaid_api_client.accounts_get(request)
    return accounts_response.accounts

def get_institution(institution_id):
    request = InstitutionsGetByIdRequest(institution_id=institution_id, country_codes=[CountryCode('US')])
    institution_response = plaid_api_client.institutions_get_by_id(request)
    return institution_response