from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from serializers import RegistrationSerializer
from dependencies import get_connection, hash_psw
from models import Users

router = APIRouter(tags=['registration'], prefix='/registration')

@router.post('/create_user', response_class=ORJSONResponse) #--> маршрут регистрации находится в разработке
async def create_user(registration_information: RegistrationSerializer, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.email == registration_information.email)
    result = (await session.execute(query))
    user = result.first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User with current email already exists"
        )
    
    salt, psw = hash_psw(registration_information.password)
    user_id = await Users.create_user(
        registration_information.username, 
        email=registration_information.email,
        psw=psw, salt=salt,
        session=session
    )
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Something went wrong. User can't be created"
        )
    return {"user_id": user_id}


@router.post('/check_username', response_class=ORJSONResponse)
async def check_username(username: str, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.username == username)
    result = await session.execute(query)
    user = result.first()
    if user: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST, 
            detail='User with current username already exists'
        )
    
    return {'exists': False}

@router.post('check_email', response_class=ORJSONResponse)
async def check_email(email: str, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.email == email)
    result = (await session.execute(query))
    user = result.first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="User with current email already exists"
        )
    return {'exists': False}