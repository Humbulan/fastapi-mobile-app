from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.routers import calculations, text_utils, auth

app = FastAPI(title="FastAPI Mobile App", version="1.0.0")

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(calculations.router, prefix="/api")
app.include_router(text_utils.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/square")
async def square_page():
    return {"message": "Square calculator page - use /api/square/{number}"}

@app.get("/reverse")
async def reverse_page():
    return {"message": "Text reverser page - use /api/reverse/{text}"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI mobile app is running"}
