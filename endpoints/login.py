
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import ORJSONResponse
from datetime import timedelta

from dependencies import check_user_credentials
from dependencies import set_token
from dependencies import get_connection
from serializers import LoginSerializer
from serializers.user import UserSerializer
from settings import auth_settings
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(tags=['login'], prefix='/login')

@router.post('/check_credentials', response_model = LoginSerializer, response_class=ORJSONResponse) #--> маршрут для проверки введенных данных при авторизации
async def check_user(auth_information: LoginSerializer, current_user: Annotated[UserSerializer, Depends(check_user_credentials)], session: AsyncSession = Depends(get_connection)):
    print(current_user)
    if not current_user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong username or password', 
            headers={"WWW-Authentificate": "Bearer"},
        )
    
    token_expire_time = timedelta(minutes=auth_settings.ACCESS_TOKEN)
    main_token = set_token(
        main_data={"username": current_user.surname},
        current_timedelta=token_expire_time
    )

    return main_token
    