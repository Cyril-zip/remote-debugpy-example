from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import notes, ping
from app.db import engine, metadata, database

metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Starting up...")
        await database.connect()
        yield
    finally:
        print("Shutting down...")
        await database.disconnect()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
