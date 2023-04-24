# Copyright 2020 Google LLC
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

# [START cloudrun_deployment_preview_dockerfile]
# Start from a Python base container
FROM python:3.11-slim

# Copy local code into the container image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Run the CLI
ENTRYPOINT ["python3", "/app/check_status.py"]
# [END cloudrun_deployment_preview_dockerfile]
