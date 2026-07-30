# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

