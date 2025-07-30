from pydantic import BaseModel
from typing import Optional

class RegistrationSerializer(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]