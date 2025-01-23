from app.api.models import NoteSchema
from app.db import notes, database, SessionLocal, engine
from datetime import datetime as dt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


async def post(payload: NoteSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = notes.insert().values(title=payload.title,
                                  description=payload.description, completed=payload.completed,
                                  created_date=created_date)
    return await database.execute(query=query)


async def get(id: int):
    query = notes.select().where(id == notes.c.id)
    return await database.fetch_one(query=query)

# WithConnectionExhaustion


async def getWithSessionBugVersion(id: int):
    # Simulate a missing session close to exhaust the connection pool
    session = SessionLocal()
    try:
        # add logpoint here to monitor the no of connection and observe the remaining connection
        result = session.execute(
            text("SELECT * FROM notes WHERE id = :id"), {"id": id}).fetchone()
        return result
    finally:
        pass
        # session.close()


async def getWithSession(id: int):
    # Simulate a missing session close to exhaust the connection pool
    session = SessionLocal()
    with SessionLocal() as session:
        result = session.execute(
            text("SELECT * FROM notes WHERE id = :id"), {"id": id}).fetchone()
        return result


async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=NoteSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        notes.update().where(id == notes.c.id).values(title=payload.title,
                                                      description=payload.description,
                                                      completed=payload.completed,
                                                      created_date=created_date)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = notes.delete().where(id == notes.c.id)
    return await database.execute(query=query)


async def get_completed(completed: str = "True"):
    query = notes.select().where(notes.c.completed == completed)
    return await database.fetch_all(query=query)


async def get_not_completed(not_completed: str = "False"):
    query = notes.select().where(notes.c.completed == not_completed)
    return await database.fetch_all(query=query)


async def get_by_title(title: str):
    query = notes.select().where(notes.c.title == title)
    return await database.fetch_all(query=query)


async def get_by_description(description: str):
    query = notes.select().where(notes.c.description == description)
    return await database.fetch_all(query=query)


async def get_by_date(created_date: str):
    query = notes.select().where(notes.c.created_date == created_date)
    return await database.fetch_all(query=query)


async def delete_all():
    query = notes.delete()
    return await database.execute(query=query)
