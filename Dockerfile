FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir grpcio==1.60.1 google-generativeai python-dotenv

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
