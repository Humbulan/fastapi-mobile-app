FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ONLY necessary files
COPY main.py .
COPY requirements.txt .

EXPOSE 8000

# Explicit command - no ambiguity
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
