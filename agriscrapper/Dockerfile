FROM python:3.9-slim

# Install necessary packages
RUN apt-get update

WORKDIR /app

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Scrapy project into the container
COPY . .

# Set the command to run your Scrapy spider
CMD ["scrapy", "crawl", "kemis_commodities_scrapper"]
