from datetime import date
from pydantic import BaseModel
from typing import Optional

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
    merchant_name: Optional[str]
    logo_url: Optional[str]
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