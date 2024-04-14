import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings
import redis.asyncio as redis


db_name = settings.db_name
db_user = settings.db_user
db_password = settings.db_password
db_host = settings.db_host
db_port = settings.db_port

redis_host = settings.redis_host
redis_port = settings.redis_port

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(engine, class_=AsyncSession,expire_on_commit=False)


# Dependency for the future
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_redis():
    r = redis.Redis(host=redis_host, port=redis_port)
    print(f"Ping successful: {await r.ping()}")
    await r.aclose()

asyncio.run(init_redis())
