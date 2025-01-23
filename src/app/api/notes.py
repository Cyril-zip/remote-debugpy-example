from app.api import crud
from app.api.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List
from datetime import datetime as dt

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await crud.post(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
        "created_date": created_date,
    }
    return response_object

@router.get("/{id}/title", response_model=str)
async def read_note(id: int = Path(..., gt=0), ):
    note = None
    try:
        note = await crud.get(id)
        return note.title # Set breakpoint and step over the code, when note id cannot be found, the function returns None and note.title will be failed
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error, please check with the support")

@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0), ):
    note = None
    try:
        note = await crud.getWithSession(id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error, please check with the support")
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/{id}/bug", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0), ):
    note = None
    try:
        note = await crud.getWithSessionBugVersion(id)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Internal Server Error, please check with the support")
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{id}/", response_model=NoteDB)
# Ensures the input is greater than 0
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note_id = await crud.put(id, payload)
    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }
    return response_object


# DELETE route
@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    await crud.delete(id)

    return note


@router.get("/completed/{completed}/", response_model=List[NoteDB])
async def read_completed_notes():
    return await crud.get_completed()


@router.get("/not_completed/{not_completed}/", response_model=List[NoteDB])
async def read_not_completed_notes():
    return await crud.get_not_completed()


@router.get("/title/{title}/", response_model=List[NoteDB])
async def read_note_by_title(title: str):
    return await crud.get_by_title(title)


@router.get("/description/{description}/", response_model=List[NoteDB])
async def read_note_by_description(description: str):
    return await crud.get_by_description(description)


@router.get("/date/{created_date}/", response_model=List[NoteDB])
async def read_note_by_date(created_date: str):
    return await crud.get_by_date(created_date)
