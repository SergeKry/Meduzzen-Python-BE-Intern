import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings
import redis.asyncio as redis

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency for the future
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_redis():
    r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    print(f"Ping successful: {await r.ping()}")
    await r.aclose()

asyncio.run(init_redis())
