FROM python:3.9-slim

# Create a non-root user
RUN useradd -m appuser

# Create a working directory
WORKDIR /app

# Copy files and install dependencies
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser snippets.py .

# Switch to the non-root user
USER appuser

# Install dependencies for the user
RUN pip install --no-cache-dir --user -r requirements.txt

# Set the entrypoint
CMD ["python3", "snippets.py"]
