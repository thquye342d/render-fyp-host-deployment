# Use official Python image
FROM python:3.12-slim

# Install OS packages needed (including libGL)
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Set working directory inside the container
WORKDIR /app

# Copy everything from your repo into the container
COPY . .

RUN pip install --upgrade pip

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Start your app (adjust if your file name or app name is different)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "Image_processing:app"]
