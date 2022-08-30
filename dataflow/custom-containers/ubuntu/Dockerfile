# Copyright 2022 Google LLC
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

FROM ubuntu:focal

WORKDIR /pipeline

# Set the entrypoint to Apache Beam SDK worker launcher.
COPY --from=apache/beam_python3.8_sdk:2.40.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Install Python with pip, dev tools, distutils, and a C++ compiler.
COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates curl g++ python3-dev python3-distutils \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    # Install the requirements.
    && pip install --no-cache-dir -r requirements.txt \
    && pip check

# Copy the pipeline source files.
COPY main.py ./
