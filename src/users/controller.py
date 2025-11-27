from  fastapi import APIRouter


router = APIRouter()

@router.get(path="/")
async def get_all():
    pass