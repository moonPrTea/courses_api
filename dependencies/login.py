from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import datetime
import jwt

from serializers import LoginSerializer

from .database import get_connection
from .password import password_functions

from settings import auth_settings
from serializers import UserSerializer
from models import Users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

async def check_user_credentials(auth_information: LoginSerializer, session: AsyncSession = Depends(get_connection)) -> UserSerializer: #--> проверка ввода корректных данных
    print(session)
    
    query = select(Users).where(Users.username == auth_information.username)
    result = await session.execute(query)
    current_user = result.all()
    
    if not current_user: 
        return None
    
    if not password_functions.check_password(auth_information.password,  current_user.password):
       return None
    print(current_user)
    
    return UserSerializer(
        username=current_user.username, password=current_user.password, email=current_user.email, 
        description=current_user.description, user_status_id=current_user.user_status_id,
        active=current_user.active, created_at=current_user.created_at, admin = current_user.admin
    )

async def set_token(main_data: dict, #--> создание токена со временем, указанным в env
                           current_timedelta: Optional[datetime.timedelta] = None):
    encode_data = main_data.copy()
    if encode_data: 
        expire_time = datetime.timezone.utc() + datetime.datetime.timestamp(minutes=current_timedelta)
    else: 
        expire_time = datetime.timezone.utc() + datetime.datetime.timestamp(minutes=auth_settings.ACCESS_TOKEN)
    
    encode_data.update({"exp": expire_time})
    return jwt.encode(encode_data, auth_settings.AUTH_KEY, algorithm=[auth_settings.ALGORITHM])


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
        username: str = data.get("username")
        if not username:
            raise exception
    except jwt.PyJWTError:
        raise exception
        
    query = select(Users).filter(Users.username == username).first()
    current_user = await session.exec(query)
    
    if not current_user: 
        raise exception
    
    return UserSerializer(
        username=current_user.username, password=current_user.password, email=current_user.email, 
        description=current_user.description, user_status_id=current_user.user_status_id,
        active=current_user.active, created_at=current_user.created_at, admin = current_user.admin
    )

    
    
    