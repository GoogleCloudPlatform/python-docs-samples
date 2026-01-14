FROM python:3.13-slim

RUN useradd -m appuser

WORKDIR /app

COPY --chown=appuser:appuser requirements.txt .

USER appuser
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser snippets.py .


CMD ["python3", "snippets.py"]
