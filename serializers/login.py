from typing import Optional
from pydantic import BaseModel


class LoginSerializer(BaseModel):
    email: Optional[str]
    password: Optional[str]