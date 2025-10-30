
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "FastAPI mobile app is running"}
