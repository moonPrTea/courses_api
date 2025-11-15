from datetime import timedelta
import select
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.login import check_input_email
from models import Users
from dependencies import check_user_credentials, get_connection, set_token
from serializers import LoginSerializer, UserSerializer, LoginEmail
from settings import auth_settings

from . import Token, TokenData, redis_functions

router = APIRouter(tags=['login'], prefix='/login')

@router.post('/check_credentials', response_class=ORJSONResponse) #--> маршрут для проверки введенных данных при авторизации
async def check_user(login_information: LoginSerializer, current_user: Annotated[UserSerializer, Depends(check_user_credentials)], 
                     session: AsyncSession = Depends(get_connection)) -> Token:
    if not current_user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong username or password', 
            headers={"WWW-Authentificate": "Bearer"},
        )
    
    token_expire_time = timedelta(minutes=auth_settings.ACCESS_TOKEN)
    main_token = await set_token(
        main_data={"username": current_user.username},
        current_timedelta=token_expire_time
    )
    
    await redis_functions.save_token(main_token, user_id=current_user.id)
    # --> сохранение токена в redis
    user_id = await redis_functions.get_user(token=main_token)
    
    
    # --> запрос с количеством активных курсов будет реализован позднее
    return Token(token=main_token, token_type="bearer", 
                 token_data=TokenData(username=current_user.username, email=current_user.email, 
                                      admin=current_user.admin))

@router.post('/check_login_email')
async def check_email(email: LoginEmail, session: AsyncSession = Depends(get_connection)):
    print(email)
    query = select(Users.id).where(Users.email == email.email)
    result = (await session.execute(query))
    user = result.first()
    
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Пользователь с данной почтой уже существует"
        )
    
    valid_email = await check_input_email(email.email)
    return valid_email