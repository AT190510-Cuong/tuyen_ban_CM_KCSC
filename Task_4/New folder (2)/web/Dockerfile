FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /app/app/static/js && \
    chmod -R 755 /app/app/static
RUN curl -L -o /app/app/static/js/purify.min.js https://unpkg.com/dompurify@latest/dist/purify.min.js

RUN chmod +x entrypoint.sh

EXPOSE 80

ENTRYPOINT ["./entrypoint.sh"]
