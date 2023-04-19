# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudrun_fs_dockerfile]
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update -y && apt-get install -y \
    tini \
    nfs-common \
    && apt-get clean

# Set fallback mount directory
ENV MNT_DIR /mnt/nfs/filestore

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Ensure the script is executable
RUN chmod +x /app/run.sh

# Use tini to manage zombie processes and signal forwarding
# https://github.com/krallin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]

# Pass the startup script as arguments to tini
CMD ["/app/run.sh"]
# [END cloudrun_fs_dockerfile]