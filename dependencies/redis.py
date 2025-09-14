# -> сохранение текущего токена в redis
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import json
from redis.asyncio import ConnectionPool, Redis
from redis.exceptions import ConnectionError

from . import get_redis_token

class RedisFunctions:
    def __init__(self) -> None:
        self.url = get_redis_token()
        self._pool: ConnectionPool = self._init_pool()
        print(self._pool)
    
    def _init_pool(self) -> ConnectionPool:
        return ConnectionPool.from_url(url=self.url, encoding='utf-8',
                                       max_connections= 10,
            socket_connect_timeout=5,
            socket_timeout=5)
    
    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator:
        current_client = Redis.from_pool(connection_pool=self._pool)
        try: 
            await current_client.ping()
            yield current_client
        except ConnectionError:
            raise 
        finally:
            await current_client.aclose()
    
    async def save_token(self, token: str, user_id: int) -> None:
        async with self.get_session() as session:
            data = {
                "user_id": user_id, 
            }
            await session.set(token, json.dumps(data))
        
    async def get_user(self, token: str):
        async with self.get_session() as session:
            data = await session.get(token)
            if not data:
                return None
            
            data = data.decode('utf-8')
            
            try:
                new_dict = json.loads(data)
                return new_dict.get('user_id')
            except Exception as e:
                return None
    
    async def delete_token(self, token: str): 
        async with self.get_session() as session: 
            return await session.delete(token) > 0


redis_functions = RedisFunctions()