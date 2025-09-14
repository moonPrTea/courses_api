from typing import Optional
from pydantic import BaseModel


class UserSerializer(BaseModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[str]
    description: Optional[str] = None
    user_status_id: Optional[int] = None
    active: Optional[bool] = None
    created_at: Optional[str]
    admin: Optional[bool]
    
