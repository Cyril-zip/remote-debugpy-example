import os
from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData, Boolean)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from sqlalchemy.orm import sessionmaker
from pytz import timezone as tz

load_dotenv("app/.env")
# Database url if none is passed the default one is used
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
POSTGRES_USER = os.getenv("POSTGRES_USER", "")
POSTGRES_DB = os.getenv("POSTGRES_DB", "")
POSTGRES_URL = os.getenv("POSTGRES_URL", "").replace("<POSTGRES_PASSWORD>", POSTGRES_PASSWORD).replace("<POSTGRES_HOST>", POSTGRES_HOST).replace("<POSTGRES_USER>", POSTGRES_USER).replace("<POSTGRES_DB>", POSTGRES_DB)



# SQLAlchemy
engine = create_engine(
    POSTGRES_URL, 
    pool_size=5,  # Limit the connection pool to 5 connections
    max_overflow=0, # No additional connections beyond the pool size
    pool_recycle=3600
) 

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed", Boolean, default=False),
    Column("created_date", String(50), default=dt.now(tz("Africa/Nairobi")).strftime("%Y-%m-%d %H:%M"))
)
# Databases query builder
database = Database(POSTGRES_URL)
