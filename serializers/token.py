from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    token: Optional[str]
    token_type: Optional[str] = 'main'

class TokenData(BaseModel):
    username: Optional[str]
    email: Optional[str] = None
    admin: Optional[bool]