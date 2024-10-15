from datetime import date

from pydantic import BaseModel
from typing import Optional

class PublicTokenRequest(BaseModel):
    public_token: str

class AccountDetailResponse(BaseModel):
    transaction_id: str
    account_name: str
    account_official_name: Optional[str]
    amount: float
    date: date
    description: str
    merchant_name: Optional[str]
    logo_url: Optional[str]
    currency: Optional[str]
    pending: bool

class BankAccountsResponse(BaseModel):
    account_id: str
    account_name: str
    account_official_name: str
    institution_name: Optional[str]
    account_mask: Optional[str]
