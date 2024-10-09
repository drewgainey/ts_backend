from fastapi import APIRouter

from db.fields import get_all_fields

router = APIRouter(prefix='/fields', tags=['fields'])

@router.get(path='')
def get_fields():
    response = get_all_fields()
    return response