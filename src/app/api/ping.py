from fastapi import APIRouter

router = APIRouter()


@router.get("/ping")
async def pong():
    # some async operation could happen here
    # example: `notes = await get_all_notes()`
    return {"ping": "pong!"}

@router.get("/debug")
async def debug():
    import debugpy
    debugpy.listen(("127.0.0.1", 5678))
    return {"debug": "started"}