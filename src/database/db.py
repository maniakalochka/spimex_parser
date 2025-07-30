from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from core.config import settings

engine = create_async_engine(
    url=settings.DB_URL,
    echo=True,
    poolclass=NullPool,

)

SessionLocal = async_sessionmaker(engine)
