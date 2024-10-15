from pydantic import BaseModel

class TransactionMatch(BaseModel):
    erp_transaction_id: int
    transaction_id: int
    amount: float