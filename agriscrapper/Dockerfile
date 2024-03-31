FROM python:3.10-alpine

WORKDIR /app

# Create a non-root user and group
RUN addgroup myuser

RUN adduser -S myuser -G myuser

# Install cron and other necessary utilities
RUN apk add --no-cache busybox-initscripts openrc && \
    rc-update add crond && \
    echo "myuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN rc-service crond start && rc-update add crond

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY  crawl.sh .

RUN chmod a+x crawl.sh

# Change the ownership to the created user and group
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

COPY . .

# Add cron job to run the crawl script every evening
RUN echo "0 18 * * * crawl.sh" | crontab -

CMD ["crond", "-f", "-d", "8"]