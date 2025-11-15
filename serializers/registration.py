from pydantic import BaseModel
from typing import Optional

class RegistrationSerializer(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
      
class ValidationAnswer(BaseModel):
    success: bool
    detail: Optional[str] = ""
    
class Username(BaseModel):
    username: str

class Email(BaseModel):
    email: str
    
class Password(BaseModel):
    password: str