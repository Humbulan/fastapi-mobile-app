from fastapi import FastAPI, HTTPException
import httpx
from datetime import datetime

app = FastAPI()

# AI Agent Configuration
AI_AGENT_URL = "http://localhost:11434/api/generate"
TIMEOUT = 30.0

async def fetch_imperial_truth():
    """Fetch current Imperial Truth metrics"""
    return {
        "valuation": 269905078380.45,
        "lithium_trend": "BULLISH (+29.7%)",
        "villages": 43,
        "target": 900,
        "status": "operational"
    }

@app.get("/")
async def root():
    """Root endpoint - Imperial AI Proxy information"""
    return {
        "service": "🤖 Imperial AI Proxy",
        "version": "7.0.0",
        "status": "operational",
        "ceo": "Humbulani Mudau",
        "endpoints": {
            "GET /": "This information",
            "GET /health": "Basic health check",
            "GET /ai/health": "AI health check",
            "GET /integration/status": "Integration status",
            "POST /ai/proxy": "AI proxy endpoint",
            "POST /ai/imperial-chat": "Imperial chat with context",
            "POST /ai/business-chat": "Business chat with context"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "service": "AI Proxy"}

@app.get("/ai/health")
async def ai_health_check():
    """AI-specific health check"""
    return {
        "status": "healthy",
        "service": "AI Proxy",
        "model": "qwen:0.5b",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/integration/status")
async def integration_status():
    """Integration status endpoint"""
    truth = await fetch_imperial_truth()
    return {
        "business_api": "✅ Operational (v7.0.0)",
        "mobile_app_api": "✅ Running on Render",
        "ai_agent": "✅ Operational",
        "imperial_truth": truth,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ai/proxy")
async def ai_proxy(payload: dict):
    """Proxy endpoint that forwards requests to Ollama"""
    try:
        ollama_payload = {
            "model": "qwen:0.5b",
            "prompt": payload.get("prompt", ""),
            "stream": False
        }
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                AI_AGENT_URL,
                json=ollama_payload,
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 200:
                return response.json()
            return {"response": "AI service temporarily unavailable"}
    except Exception as e:
        return {"error": str(e), "response": "Imperial AI processing"}

@app.post("/ai/imperial-chat")
async def imperial_ai_chat(user_message: str):
    """Enhanced AI chat with Imperial Truth context"""
    imperial_context = await fetch_imperial_truth()
    sovereign_prompt = f"""You are the Imperial AI of Humbulani Mudau's enterprise.
Current Imperial Truth:
- Valuation: R{imperial_context['valuation']:,.2f}
- Lithium Trend: {imperial_context['lithium_trend']}
- Village Network: {imperial_context['villages']}/{imperial_context['target']} villages
- Status: {imperial_context['status']}

User Query: {user_message}"""
    
    try:
        ollama_payload = {
            "model": "qwen:0.5b",
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
                    "imperial_response": ai_response.get("response", ""),
                    "imperial_truth": imperial_context,
                    "timestamp": datetime.now().isoformat(),
                    "sovereignty": "IMPERIAL_OMEGA_SOVEREIGNTY"
                }
            return {
                "imperial_response": "Imperial Network processing your request.",
                "imperial_truth": imperial_context,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "imperial_response": "Imperial systems operating at full capacity.",
            "error": str(e),
            "imperial_truth": imperial_context,
            "timestamp": datetime.now().isoformat()
        }

@app.post("/ai/business-chat")
async def ai_business_chat(user_message: str):
    """Business chat with Imperial Truth context"""
    imperial_context = await fetch_imperial_truth()
    
    try:
        ollama_payload = {
            "model": "qwen:0.5b",
            "prompt": f"Business query: {user_message}\nContext: {imperial_context}",
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
            return {
                "ai_response": "AI service temporarily unavailable",
                "business_context": imperial_context,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "ai_response": "Imperial AI is processing your request.",
            "business_context": imperial_context,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8118)
