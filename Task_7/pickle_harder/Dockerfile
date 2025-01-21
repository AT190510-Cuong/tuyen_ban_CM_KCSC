FROM python:3.10-slim

ENV USER=user

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /app

COPY --chown=$USER:$USER ./app /app

RUN useradd --no-log-init --create-home --shell /bin/bash $USER && \
    chown -R $USER:$USER /app

USER $USER

EXPOSE 5000

CMD ["python", "app.py"]
