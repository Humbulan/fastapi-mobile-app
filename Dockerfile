# Stage 1: Build Stage - Use a lightweight Python base image
FROM python:3.11-slim AS builder

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Production Stage - Use the same clean base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the rest of the application code
COPY . /app

# Expose the port where the Uvicorn/Gunicorn process will run
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application using Uvicorn directly (simpler for now)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
