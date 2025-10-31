from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.mongodb import get_user_by_username, premium_data_collection
from datetime import datetime

router = APIRouter()
security = HTTPBearer()
SECRET_KEY = "your-secret-key-change-in-production-mongodb-12345"
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
    # Check if user has premium access
    user = await get_user_by_username(current_user)
    if not user or not user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail="Premium feature requires upgrade. Visit /api/auth/upgrade-premium"
        )
    
    try:
        # Safe evaluation (in production, use a proper math parser)
        result = eval(expression)
        
        # Save calculation history to MongoDB
        await premium_data_collection.insert_one({
            "username": current_user,
            "feature": "advanced_calculator",
            "expression": expression,
            "result": result,
            "timestamp": datetime.utcnow()
        })
        
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
    # Check if user has premium access
    user = await get_user_by_username(current_user)
    if not user or not user.get("premium", False):
        raise HTTPException(
            status_code=403, 
            detail="Premium feature requires upgrade"
        )
    
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
    
    # Save conversion to MongoDB
    await premium_data_collection.insert_one({
        "username": current_user,
        "feature": "currency_conversion",
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
        "converted_amount": converted_amount,
        "timestamp": datetime.utcnow()
    })
    
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
    user = await get_user_by_username(current_user)
    if not user or not user.get("premium", False):
        raise HTTPException(status_code=403, detail="Premium feature requires upgrade")
    
    # Get user's premium usage stats from MongoDB
    user_calculations = await premium_data_collection.count_documents({
        "username": current_user,
        "feature": "advanced_calculator"
    })
    
    user_conversions = await premium_data_collection.count_documents({
        "username": current_user,
        "feature": "currency_conversion"
    })
    
    return {
        "user": current_user,
        "premium_since": user.get("updated_at", "Recently"),
        "advanced_calculations": user_calculations,
        "currency_conversions": user_conversions,
        "total_premium_uses": user_calculations + user_conversions,
        "premium": True
    }
