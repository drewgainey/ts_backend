from fastapi import APIRouter, HTTPException

from db import match_transactions
from models import TransactionMatch
from typing import List

router = APIRouter(prefix="/match", tags=["match"])

@router.post(path='')
async def match_transactions(matches: List[TransactionMatch]):
    try:
        await match_transactions(matches)
        return {"status": "success", "message": f"Inserted {len(matches)} transaction matches successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))