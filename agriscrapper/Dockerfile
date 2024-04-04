FROM python:3.9-slim

# Install necessary packages
RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Scrapy
RUN pip install scrapy

# Copy your Scrapy project into the container
COPY . .

# Optionally, if you have scrapy settings and pipelines
# you want to include, you can copy them as well
# COPY settings.py /app
# COPY pipelines.py /app

# Set the command to run your Scrapy spider
CMD ["scrapy", "crawl", "your_spider_name"]
