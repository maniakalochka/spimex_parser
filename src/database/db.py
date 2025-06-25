from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from models.base import Base

engine = create_engine(
    url=settings.DB_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
