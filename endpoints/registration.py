from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse

from serializers import RegistrationSerializer
from dependencies import get_connection, password_functions

router = APIRouter(tags=['registration'], prefix='/registration')

@router.post('/create_user', response_model = RegistrationSerializer, response_class=ORJSONResponse) #--> маршрут регистрации находится в разработке
async def create_user(registration_information: RegistrationSerializer, session: AsyncSession = Depends(get_connection)):
    print(registration_information)
    print(password_functions.create_password(registration_information.password))
    return registration_information