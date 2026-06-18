from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import secrets
import os
from datetime import datetime
from typing import Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBasic(auto_error=False)

def optional_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials:
        correct_username = secrets.compare_digest(credentials.username, "humbulani")
        correct_password = secrets.compare_digest(credentials.password, os.getenv("SECURE_PASSWORD", "imperial2026"))
        if correct_username and correct_password:
            logger.info(f"Admin access granted: {credentials.username}")
            return {"role": "admin", "username": credentials.username}
    return {"role": "public", "username": "visitor"}

app = FastAPI(
    title="Imperial AI Nexus - Humbulani Mudau",
    description="Enterprise AI Chat Interface with Imperial Truth Integration",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

AI_AGENT_URL = "http://127.0.0.1:8118/ai/proxy"
TIMEOUT = 120.0

@app.get("/api/imperial/truth")
async def get_imperial_truth():
    return {
        "valuation": 269905078380.45,
        "lithium_trend": "BULLISH (+29.7%)",
        "villages": 43,
        "target": 900,
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.api_route("/ai/imperial-chat", methods=["GET", "POST"])
async def imperial_ai_chat(user_message: str):
    try:
        imperial_context = await get_imperial_truth()
        sovereign_prompt = f"""You are the Imperial AI. 
Current Imperial Truth:
- Valuation: R{imperial_context['valuation']:,.2f}
- Lithium Trend: {imperial_context['lithium_trend']}
- Village Network: {imperial_context['villages']}/{imperial_context['target']}
- Status: {imperial_context['status']}
User Query: {user_message}"""
        ollama_payload = {"model": "my-model", "prompt": sovereign_prompt, "stream": False}
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(AI_AGENT_URL, json=ollama_payload, headers={"Content-Type": "application/json"})
            if response.status_code == 200:
                ai_response = response.json()
                return {"ai_response": ai_response.get("response", ""), "business_context": imperial_context, "timestamp": datetime.now().isoformat()}
            else:
                return {"ai_response": "Imperial AI systems are processing.", "business_context": imperial_context, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        return {"ai_response": "I'm here to assist.", "error": str(e), "timestamp": datetime.now().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def serve_chat_interface():
    try:
        with open("public/ai-chat.html", "r") as f:
            return HTMLResponse(content=f.read())
    except:
        return HTMLResponse("<h1>Imperial AI Nexus</h1><p>Interface loading...</p>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/api/trade/total")
async def get_dummy_trade_total():
    return {"status": "monitored", "total_trade": 0.0}
