# ==============================================================================
# Cognitive Entanglement - Containerized Microservice Deployment Dockerfile 🐋⚙️
# Language: Dockerfile / YAML
# ==============================================================================

FROM python:3.10-slim-bullseye

# Set system variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system and C++ build requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libportaudio2 \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project source code tree
COPY . /app/

# Expose Web dashboard telemetery port
EXPOSE 5000

# Start Flask-SocketIO Cognitive server
CMD ["python", "src/dashboard.py"]
