from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_connection, hash_psw
from helpers import check_input_email, check_input_username, check_input_password
from models import Users
from serializers import RegistrationSerializer, Username, Email, Password

router = APIRouter(tags=['registration'], prefix='/registration')

@router.post('/check_email')
async def check_email(email: Email, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.email == email.email)
    result = (await session.execute(query))
    user = result.first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Пользователь с данной почтой уже существует"
        )
    
    valid_email = await check_input_email(email.email)
    print(valid_email)
    return valid_email

@router.post('/check_username')
async def check_username(username: Username, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.username == username.username)
    result = await session.execute(query)
    user = result.first()
    if user: 
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail='Пользователь с данным username существует'
        )
    
    valid_username = await check_input_username(username.username)  
    return valid_username


@router.post('/check_password')
async def check_password(password: Password, session: AsyncSession = Depends(get_connection)):
    return await check_input_password(password.password)


@router.post('/create_user', response_class=ORJSONResponse)  # --> маршрут регистрации находится в разработке
async def create_user(registration_information: RegistrationSerializer, session: AsyncSession = Depends(get_connection)):
    query = select(Users).where(Users.email == registration_information.email)
    result = (await session.execute(query))
    user = result.first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Пользователь с данной почтой существует"
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
            detail="Что-то пошло не так. Аккаунт не был создан"
        )
    return {"user_id": user_id}