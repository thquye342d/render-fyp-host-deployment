# Use official Python image
FROM python:3.12-slim

# Install OS packages needed (libGL + basic libraries)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy all your code to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start your app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Image_processing:app"]
