from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.routers import calculations, text_utils, auth
from jose import JWTError, jwt
import time
import os

app = FastAPI(title="FastAPI Mobile App", version="2.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Security
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

# Include routers
app.include_router(calculations.router, prefix="/api")
app.include_router(text_utils.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(premium.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/premium")
async def premium_page():
    return {"message": "Premium features coming soon!"}

@app.get("/health", status_code=200)
async def health_check():
    return {
        "status": "healthy", 
        "message": "FastAPI mobile app is running",
        "version": "2.0.0",
        "timestamp": time.time()
    }

@app.get("/health/simple", status_code=200)
async def simple_health_check():
    return {"status": "ok", "message": "Service is running"}
