import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings


db_name = settings.db_name
db_user = settings.db_user
db_password = settings.db_password
db_host = settings.db_host
db_port = settings.db_port

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def async_main() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    await engine.dispose()


asyncio.run(async_main())

