# Dockerfile

# Use Python 3.13 slim image for a smaller footprint
FROM python:3.13-slim

# Install minimal system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install --no-cache-dir -U pip setuptools wheel && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application with explicit Python path
CMD ["/usr/local/bin/python", "app.py"]
