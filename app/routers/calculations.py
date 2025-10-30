from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class SquareRequest(BaseModel):
    number: float

@router.post("/square")
async def square_number(request: SquareRequest):
    return {"result": request.number ** 2}

@router.get("/square/{number}")
async def square_get(number: float):
    return {"result": number ** 2}
