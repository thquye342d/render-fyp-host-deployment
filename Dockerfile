FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
