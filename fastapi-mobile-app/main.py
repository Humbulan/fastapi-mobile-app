from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
import httpx
import secrets
import os
from datetime import datetime
from typing import Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imperial Gatekeeper - Optional for AI chat
security = HTTPBasic(auto_error=False)

def optional_auth(credentials: HTTPBasicCredentials = Depends(security)):
    """Optional authentication - allows public access to AI chat"""
    if credentials:
        correct_username = secrets.compare_digest(credentials.username, "humbulani")
        correct_password = secrets.compare_digest(credentials.password, os.getenv("SECURE_PASSWORD", "imperial2026"))
        if correct_username and correct_password:
            logger.info(f"Admin access granted: {credentials.username}")
            return {"role": "admin", "username": credentials.username}
    return {"role": "public", "username": "visitor"}

# Create FastAPI app
app = FastAPI(
    title="Imperial AI Nexus - Humbulani Mudau",
    description="Enterprise AI Chat Interface with Imperial Truth Integration",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# AI Agent Configuration
AI_AGENT_URL = "http://127.0.0.1:8118/ai/proxy"  # Routed through AI Proxy Gateway
TIMEOUT = 120.0

# Imperial Truth endpoint
@app.get("/api/imperial/truth")
async def get_imperial_truth():
    """Return current Imperial Truth metrics"""
    return {
        "valuation": 269905078380.45,
        "lithium_trend": "BULLISH (+29.7%)",
        "villages": 43,
        "target": 900,
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

# AI Chat endpoint (public)
@app.post("/ai/chat")
async def ai_chat(message_data: dict):
    """Public AI chat endpoint"""
    try:
        # Fetch the complete live operational context data
        truth_data = await get_imperial_truth()
        user_msg = message_data.get("message", "")
        
        # Build the structured system data feed context
        enriched_prompt = (
            f"[SYSTEM DATA FEED - IMPERIAL VILLAGE REGISTRY REAL DATA]\n"
            f"- Active Network Architecture: Imperial Omega (SADC Corridor)\n"
            f"- Total Verified Infrastructure Nodes: 18 Active Nodes (Thohoyandou, Sibasa, Malamulele, Lwamondo, Manini, Mukhomi, etc.)\n"
            f"- Total Verified Users: 900 Users (Vault Sentry Verified across all layers)\n"
            f"- Active Market Campaign: Village Market Artisans (Current Target: 279 Artisans, targeting 100 new referrals)\n"
            f"- Total Wealth Lock Asset Valuation: R269,903,984,698.71 ZAR (Verified)\n"
            f"- SADC Corridor Logistics Capacity: Active Beira Port Expansion (14.2M / 18M Tons)\n"
            f"- System Baseline Status: {truth_data.get("status", "operational")}\n\n"
            f"[BUSINESS DIRECTIVE]\n"
            f"{user_msg}\n\n"
            f"Provide an explicit, quantitative audit response based strictly on the verified registry metrics above. Do not invent populations or extrapolate fictional data."
        )

        ollama_payload = {
            "model": "qwen2.5:0.5b",
            "prompt": enriched_prompt,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=ollama_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                ollama_response = response.json()
                return {
                    "response": ollama_response.get("response", ""),
                    "model": ollama_response.get("model", "qwen:0.5b"),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "response": "Imperial AI is currently optimizing. Please try again.",
                    "model": "fallback",
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "response": "I'm here to assist with your enterprise queries.",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Enhanced Imperial Chat with business context
@app.api_route("/ai/imperial-chat", methods=["GET", "POST"])
async def imperial_ai_chat(user_message: str):
    """Enhanced AI chat with Imperial Truth context"""
    try:
        # Get imperial truth
        imperial_context = await get_imperial_truth()
        
        sovereign_prompt = f"""You are the Imperial AI of Humbulani Mudau's enterprise.
Current Imperial Truth:
- Valuation: R{imperial_context['valuation']:,.2f}
- Lithium Trend: {imperial_context['lithium_trend']}
- Village Network: {imperial_context['villages']}/{imperial_context['target']} villages
- Status: {imperial_context['status']}

User Query: {user_message}

Provide a helpful response as the Imperial AI assistant."""
        
        ollama_payload = {
            "model": "qwen2.5:0.5b",
            "prompt": sovereign_prompt,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=ollama_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                ai_response = response.json()
                return {
                    "ai_response": ai_response.get("response", ""),
                    "business_context": imperial_context,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "ai_response": "Imperial AI systems are processing your request.",
                    "business_context": imperial_context,
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "ai_response": "I'm here to assist with your enterprise questions.",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

# Serve AI chat as homepage
@app.get("/", response_class=HTMLResponse)
async def serve_chat_interface(auth=Depends(optional_auth)):
    """Serve the AI chat interface as the main page"""
    try:
        with open("public/ai-chat.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head><title>Imperial AI Nexus</title></head>
        <body style="font-family: monospace; padding: 40px; background: #0d1117; color: white;">
            <h1>🤖 Imperial AI Nexus</h1>
            <p>Chat interface loading... Please refresh.</p>
        </body>
        </html>
        """)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Imperial AI Nexus",
        "version": "3.0.0",
        "timestamp": datetime.now().isoformat()
    }

# Imperial AI Dashboard Route
@app.get("/dashboard")
async def ai_dashboard():
    from fastapi.responses import HTMLResponse
    try:
        with open("../templates/ai_dashboard.html", "r") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>AI Dashboard Error</h1><p>{str(e)}</p>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8118)

# Add this near the top with other imports if not already there
import asyncio

@app.post("/ai/proxy")
async def render_ai_proxy(payload: dict):
    """
    Proxy endpoint on Render that forwards to your local AI through tunnel
    This creates a reliable bridge between Render and your local AI
    """
    # Your tunnel URL
    TUNNEL_URL = "https://ai.humbu.store/ai/proxy"
    
    for attempt in range(3):  # Retry up to 3 times
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.post(
                    TUNNEL_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    # Return a graceful error
                    return {
                        "response": "AI service is warming up. Please try again in a moment.",
                        "status": "degraded",
                        "attempt": attempt + 1
                    }
        except Exception as e:
            if attempt == 2:  # Last attempt failed
                return {
                    "response": "Imperial AI is processing your request. The network is stable.",
                    "error": str(e),
                    "status": "fallback"
                }
            await asyncio.sleep(1)  # Wait before retry

# Update the imperial-chat endpoint to use this proxy
# Find the imperial_ai_chat function and replace its content with:
"""
    try:
        # Call the proxy endpoint instead of directly calling the tunnel
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "qwen2.5:0.5b",
                    "prompt": user_message,
                    "stream": False
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "ai_response": data.get("response", "Processing..."),
                    "business_context": await get_imperial_truth(),
                    "timestamp": datetime.now().isoformat()
                }
    except Exception as e:
        return {
            "ai_response": "Imperial systems are operating at full capacity.",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
"""

# Added to silence automated dashboard log spam
@app.get("/api/trade/total")
async def get_dummy_trade_total():
    return {"status": "monitored", "total_trade": 0.0}

# Added to silence automated dashboard log spam
@app.get("/api/trade/total")
async def get_dummy_trade_total():
    return {"status": "monitored", "total_trade": 0.0}
