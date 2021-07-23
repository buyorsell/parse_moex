from sqlalchemy import (
    create_engine,

    Column,

    Integer,
    Float,
    String,
    DateTime

)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os, asyncio


Base = declarative_base()


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    boardid = Column(String)
    date = Column(DateTime)
    secid = Column(String)
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    numtrades = Column(Integer)


class Ticker(Base):
	__tablename__ = 'tickers'
	id = Column(Integer, primary_key=True)
	sec_id = Column(String)
	shortname = Column(String)
	bos = Column(Float)

async_engine = create_async_engine(
    os.environ.get('PSQL_DB')
)
async def create_all(engine, meta):
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

#Base.metadata.bind = async_engine
#Base.metadata.create_all(async_engine)


async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
#Base.metadata.bind = sync_engine
#Base.metadata.create_all(sync_engine)

#SyncDBSession = sessionmaker(bind=sync_engine)
#sync_session = SyncDBSession()
#asyncio.run(create_all(async_engine, Base.metadata))
