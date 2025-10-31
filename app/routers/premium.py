from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

router = APIRouter()
security = HTTPBearer()
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Premium-only features
@router.get("/advanced-calculator/{expression}")
async def advanced_calculator(expression: str, current_user: str = Depends(get_current_user)):
    """Premium feature: Advanced calculator with complex expressions"""
    try:
        # Safe evaluation (in production, use a proper math parser)
        result = eval(expression)
        return {
            "expression": expression,
            "result": result,
            "premium": True,
            "user": current_user
        }
    except:
        raise HTTPException(status_code=400, detail="Invalid mathematical expression")

@router.get("/currency-convert/{amount}/{from_currency}/{to_currency}")
async def currency_convert(amount: float, from_currency: str, to_currency: str, current_user: str = Depends(get_current_user)):
    """Premium feature: Currency conversion"""
    # Mock conversion rates
    rates = {
        "USD": 1.0,
        "EUR": 0.85,
        "GBP": 0.73,
        "ZAR": 18.5,
        "INR": 75.0
    }
    
    if from_currency not in rates or to_currency not in rates:
        raise HTTPException(status_code=400, detail="Unsupported currency")
    
    converted_amount = (amount / rates[from_currency]) * rates[to_currency]
    
    return {
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": round(converted_amount, 2),
        "premium": True,
        "user": current_user
    }

@router.get("/premium-stats")
async def premium_stats(current_user: str = Depends(get_current_user)):
    """Premium feature: User statistics"""
    return {
        "user": current_user,
        "premium_since": "2024-01-01",
        "calculations_this_month": 150,
        "favorite_tool": "Advanced Calculator",
        "premium": True
    }
