from fastapi import APIRouter

from . import redis_functions

router = APIRouter(tags=['token'], prefix='/token')

@router.post('/delete/{token}')
async def delete_token(token: str):
    success = await redis_functions.delete_token(token)
    if success:
        return {"success": True}
    return {"success": False}