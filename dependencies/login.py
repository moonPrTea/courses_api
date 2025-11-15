from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from serializers import LoginSerializer, UserSerializer
from settings import auth_settings

from . import Users
from .database import get_connection
from .password import is_correct_psw


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def check_user_credentials(login_information: LoginSerializer, session: AsyncSession = Depends(get_connection)) -> UserSerializer: #--> проверка ввода корректных данных
    
    query = select(Users).where(Users.email == login_information.email)
    result = await session.execute(query)
    current_user = result.scalars().first()
    
    if not current_user: 
        return None
    
    if not is_correct_psw(current_user.salt,  current_user.password, login_information.password):
        return None
    
    return UserSerializer(
        id = current_user.id,
        username=current_user.username, password=current_user.password, email=current_user.email, 
        description=current_user.description, user_status_id=current_user.user_status_id,
        active=current_user.active, created_at=None, admin = current_user.admin
    )
    

async def set_token(main_data: dict, #--> создание токена со временем, указанным в env
                           current_timedelta: Optional[timedelta] = None):
    encode_data = main_data.copy()
    if encode_data: 
        expire_time = datetime.now(timezone.utc) + current_timedelta
    else: 
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=auth_settings.ACCESS_TOKEN)
    
    encode_data.update({"exp": expire_time})
    return jwt.encode(encode_data, auth_settings.AUTH_KEY, algorithm=auth_settings.ALGORITHM)


async def get_current_user( #--> получение данных о текущем пользователе из токена
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_connection)
) -> UserSerializer:
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = "Not validated credentials"
        )
    try: 
        data = jwt.decode(token, auth_settings.AUTH_KEY, algorithms=[auth_settings.ALGORITHM])
        email: str = data.get("email")
        if not email:
            raise exception
    except jwt.PyJWTError:
        raise exception
        
    query = select(Users).filter(Users.email == email).first()
    current_user = await session.exec(query)
    
    if not current_user: 
        raise exception
    
    return UserSerializer(
        id = current_user.id,
        username=current_user.username, password=current_user.password, email=current_user.email, 
        description=current_user.description, user_status_id=current_user.user_status_id,
        active=current_user.active, created_at=current_user.created_at, admin = current_user.admin
    )
    