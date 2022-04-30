FROM python:3.9-slim

WORKDIR /app

COPY *.py ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["gunicorn", "--threads=8", "--timeout=0", "main:app"]
