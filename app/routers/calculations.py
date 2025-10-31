from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import math

router = APIRouter()

class SquareRequest(BaseModel):
    number: float

@router.post("/square")
async def square_number(request: SquareRequest):
    return {"result": request.number ** 2}

@router.get("/square/{number}")
async def square_get(number: float):
    return {"result": number ** 2}

@router.get("/multiply/{a}/{b}")
async def multiply(a: float, b: float):
    return {"result": a * b}

@router.get("/divide/{a}/{b}")
async def divide(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Cannot divide by zero")
    return {"result": a / b}

@router.get("/sqrt/{number}")
async def square_root(number: float):
    if number < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate square root of negative number")
    return {"result": math.sqrt(number)}

@router.get("/power/{base}/{exponent}")
async def power(base: float, exponent: float):
    return {"result": base ** exponent}

@router.get("/factorial/{number}")
async def factorial(number: int):
    if number < 0:
        raise HTTPException(status_code=400, detail="Cannot calculate factorial of negative number")
    if number > 50:
        raise HTTPException(status_code=400, detail="Number too large for factorial calculation")
    return {"result": math.factorial(number)}

@router.get("/percentage/{number}/{percent}")
async def percentage(number: float, percent: float):
    return {"result": (number * percent) / 100}

@router.get("/compound-interest/{principal}/{rate}/{time}")
async def compound_interest(principal: float, rate: float, time: float):
    amount = principal * ((1 + rate/100) ** time)
    interest = amount - principal
    return {
        "principal": principal,
        "rate": rate,
        "time": time,
        "final_amount": round(amount, 2),
        "interest_earned": round(interest, 2)
    }
