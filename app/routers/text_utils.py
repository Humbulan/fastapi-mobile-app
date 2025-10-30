from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class TextRequest(BaseModel):
    text: str

@router.post("/reverse")
async def reverse_text(request: TextRequest):
    return {"result": request.text[::-1]}

@router.get("/reverse/{text}")
async def reverse_get(text: str):
    return {"result": text[::-1]}
