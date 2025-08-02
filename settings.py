from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class DatabaseSettings(BaseSettings):
    DB_ADRESS: str = 'adress'
    DB_PORT: int = 0
    DB_NAME: str = 'database'
    DB_USERNAME: str = 'username'
    DB_PASSWORD: str = 'password'

db_settings = DatabaseSettings()

class AuthSettings(BaseSettings):
    AUTH_KEY: str = ''
    ALGORITHM: str = ''
    ACCESS_TOKEN: int = 0

auth_settings = AuthSettings()

class SecuritySettings(BaseSettings):
    PASSWORD_BYTES: int = 0
    PASSWORD_ALGORITHM: str = 'algorithm'
    PASSWORD_PEPPER: bytes = b'1111'

security_settings = SecuritySettings()
        
def get_database_token() -> str:
    return (f"postgresql+asyncpg://{db_settings.DB_USERNAME}:{db_settings.DB_PASSWORD}@"
            f"{db_settings.DB_ADRESS}:{db_settings.DB_PORT}/{db_settings.DB_NAME}")
    
