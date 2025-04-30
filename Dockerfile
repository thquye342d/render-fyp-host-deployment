FROM python:3.12-slim

# Install system dependencies (e.g., for OpenCV)
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 8000
EXPOSE 8000

# Run Gunicorn with timeout and optimized workers
CMD ["gunicorn", "--timeout", "60", "--workers=1", "--threads=4", "-b", "0.0.0.0:8000", "Image_processing:app"]
