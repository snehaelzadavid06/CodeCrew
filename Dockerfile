# Dockerfile

# Use Python 3.13 slim image
FROM python:3.13-slim

# Install system dependencies for PyAudio and other packages
RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    python3-dev \
    pkg-config \
    build-essential \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir PyAudio && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
