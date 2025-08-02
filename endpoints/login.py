from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from dependencies import check_user_credentials, set_token, get_connection
from serializers import UserSerializer, LoginSerializer
from settings import auth_settings
from . import Token, TokenData

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
    
    # --> запрос с количеством активных курсов будет реализован позднее
    return Token(token=main_token, token_type="bearer", 
                 token_data=TokenData(username=current_user.username, email=current_user.email, 
                                      admin=current_user.admin))