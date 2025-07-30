from typing import Optional
from pydantic import BaseModel


class LoginSerializer(BaseModel):
    username: Optional[str]
    password: Optional[str]