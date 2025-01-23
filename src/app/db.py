import os
from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData, Boolean)
from dotenv import load_dotenv
from databases import Database
from datetime import datetime as dt
from sqlalchemy.orm import sessionmaker
from pytz import timezone as tz

load_dotenv("app/.env")
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "")

# SQLAlchemy
engine = create_engine(
    DATABASE_URL, 
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
database = Database(DATABASE_URL)
