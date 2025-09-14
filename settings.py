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

class RedisSettings(BaseSettings): 
    REDIS_HOST: str = 'host'
    REDIS_PORT: int = 0
    REDIS_DB: int = 0 
    
redis_settings = RedisSettings()
        
def get_database_token() -> str:
    return (f"postgresql+asyncpg://{db_settings.DB_USERNAME}:{db_settings.DB_PASSWORD}@"
            f"{db_settings.DB_ADRESS}:{db_settings.DB_PORT}/{db_settings.DB_NAME}")

def get_redis_token() -> str:
    return (f"redis://{redis_settings.REDIS_HOST}:{redis_settings.REDIS_PORT}/{redis_settings.REDIS_DB}")
