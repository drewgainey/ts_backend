from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from pydantic import BaseModel

from .plaid_client import plaid_api_client

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