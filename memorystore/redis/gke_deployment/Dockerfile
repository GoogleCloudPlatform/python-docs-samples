# Copyright 2021 Google LLC
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

# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.14-slim

# Note: REDISHOST value here is only used for local testing
# See README.md on how to inject environment variable as ConfigMap on GKE
ENV REDISHOST 127.0.0.1
ENV REDISPORT 6379

ENV APP_HOME /app
WORKDIR $APP_HOME

# Install dependencies.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Add application code.
COPY . ./

CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
