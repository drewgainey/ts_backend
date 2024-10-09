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
    description: str
    merchant_name: Optional[str]
    logo_url: Optional[str]
    currency: Optional[str]
    pending: bool
    gl_account_number: Optional[str]
    gl_account_name: Optional[str]
