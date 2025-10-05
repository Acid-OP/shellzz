FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir \
    grpcio==1.60.1 \
    google-generativeai \
    python-dotenv

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]