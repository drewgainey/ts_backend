import os
from dotenv import load_dotenv
from plaid import Configuration, ApiClient, Environment
from plaid.api import plaid_api

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


