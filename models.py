from datetime import date

from pydantic import BaseModel
from typing import Optional

# API Requests
class PublicTokenRequest(BaseModel):
    public_token: str

class TransactionDetailResponse(BaseModel):
    transaction_id: str
    account_name: str
    account_official_name: Optional[str]
    amount: float
    date: date
    merchant_name: Optional[str]
    currency: Optional[str]
    pending: bool
    gl_account_number: Optional[str]
    gl_account_name: Optional[str]

# Used for inserting Plaid data into db
class PlaidBalance(BaseModel):
    available: float
    current: float
    iso_currency_code: str
    limit: Optional[float]
    unofficial_currency_code: Optional[str]

class PlaidTransaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    date: date
    name: str
    iso_currency_code: str
    pending: bool

class PlaidAccount(BaseModel):
    account_id: str
    balances: PlaidBalance
    mask: str
    name: str
    official_name: Optional[str]
    persistent_account_id: str
    type: str
    subtype: str






