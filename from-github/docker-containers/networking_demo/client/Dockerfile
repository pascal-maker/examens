# 1️⃣ Stage 1: Build Dependencies
FROM python:3.13.2-alpine3.21 AS builder

# Set working directory
WORKDIR /app

# Copy only requirements to leverage Docker caching
COPY requirements.txt .

# Install dependencies inside a virtual environment
RUN pip install --no-cache-dir --user -r requirements.txt

# 2️⃣ Stage 2: Final Lightweight Image
FROM python:3.13.2-alpine3.21 AS final

# Install curl
RUN apk add --no-cache curl

# Set working directory
WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY ./app .

# Set PATH to include locally installed binaries
ENV PATH="/home/appuser/.local/bin:$PATH"

# Security: Create a non-root user and switch to it
RUN adduser -D appuser
USER appuser

# Run the FastAPI application
CMD ["uvicorn", "client:app", "--host", "0.0.0.0", "--port", "80"]