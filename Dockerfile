FROM python:3.12-slim

# Install system dependencies for OpenCV and Flask
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (for caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create uploads directory (matches your Flask code)
RUN mkdir -p /app/uploads

# Expose port (must match Azure's WEBSITES_PORT)
EXPOSE 8000

# Run Gunicorn (ensure it points to "Image_processing:app")
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "--capture-output", "Image_processing:app"]
