# Use the official Python image
FROM python:3.10

# Install build essentials and spaCy dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Expose the port that Uvicorn will run on (adjust as needed)
EXPOSE 8050

CMD ["python", "app.py"]
