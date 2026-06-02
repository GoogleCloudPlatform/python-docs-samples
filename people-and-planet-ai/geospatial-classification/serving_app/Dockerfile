FROM python:3.14-slim

WORKDIR /app

COPY *.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
