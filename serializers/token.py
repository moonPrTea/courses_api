from pydantic import BaseModel
from typing import Dict, Optional

class TokenData(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    admin: Optional[bool]
    user_courses: Optional[int] = 0
    
class Token(BaseModel):
    token: Optional[str]
    token_type: Optional[str] = 'main'
    expires_time: Optional[int] = 0
    token_data: Optional[TokenData]
    
class TModel(BaseModel):
    token: str