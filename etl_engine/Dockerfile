# Use a smaller base image
FROM python:3.10-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt


# Copy the entire application code
COPY . .

# Build the final image
FROM python:3.10-slim
COPY --from=builder . .
WORKDIR /app
EXPOSE 3000
CMD ["python", "app.py"]