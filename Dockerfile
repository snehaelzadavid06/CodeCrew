# Dockerfile

# Use Python 3.13 image with required build tools
FROM python:3.13

# Install system dependencies for PyAudio and other packages
RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    python3-dev \
    pkg-config \
    build-essential \
    libasound2-dev \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with specific steps for PyAudio
RUN python -m pip install --no-cache-dir -U pip setuptools wheel && \
    python -m pip install --no-cache-dir \
        audioop_lts==0.2.1 \
        standard-aifc==3.13.0 \
        standard-chunk==3.13.0 && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application with explicit Python path
CMD ["/usr/local/bin/python", "app.py"]
