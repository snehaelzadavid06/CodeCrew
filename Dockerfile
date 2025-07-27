# Dockerfile

# Use Python 3.10 slim image
FROM python:3.10-slim

# Install system dependencies for PyAudio
RUN apt-get update && \
    apt-get install -y portaudio19-dev python3-dev gcc && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]
