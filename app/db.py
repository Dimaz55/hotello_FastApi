from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings
from app.logger import logger

if settings.MODE == "TEST":
    DB_URL = settings.TEST_DB_URL
    DB_PARAMS = {"poolclass": NullPool}
elif settings.MODE == "PROD":
    DB_URL = settings.DB_URL
    DB_PARAMS = {}
else:
    DB_URL = settings.DB_URL
    DB_PARAMS = {}

engine = None
try:
    engine = create_async_engine(DB_URL, **DB_PARAMS)
except Exception as e:
    logger.error("Database connection error", extra={
        "exception": e
    })

try:
    async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
except Exception as e:
    logger.error("async_sessionmaker error", extra={
        "exception": e
    })


class Base(DeclarativeBase):
    pass
