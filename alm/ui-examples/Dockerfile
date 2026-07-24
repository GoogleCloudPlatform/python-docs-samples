# Use a slim version to keep the image small
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# - 'curl' is required to download the gcloud SDK installer
# - 'build-essential' is kept in case any Python packages need compiling
# Note: We dropped 'jq' because Python's requests library handles JSON parsing now!
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && curl -sSL https://sdk.cloud.google.com | bash -s -- --disable-prompts \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set up the Cloud SDK path so Python's subprocess can find 'gcloud'
ENV PATH="/root/google-cloud-sdk/bin:${PATH}"

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into container
COPY . .

# Cloud Run sets the $PORT environment variable automatically
# We use exec form for the CMD to handle signals properly
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app









# # Use a slim version to keep the image small
# FROM python:3.12-slim

# # Set working directory
# WORKDIR /app

# # Prevent Python from writing .pyc files and enable unbuffered logging
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Install system dependencies (only what's necessary for your app)
# # If you don't need 'curl', 'jq', or 'gcloud' inside the running app, remove them!
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # Install Python packages
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy app code into container
# COPY . .

# # Cloud Run sets the $PORT environment variable automatically
# # We use exec form for the CMD to handle signals properly
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app