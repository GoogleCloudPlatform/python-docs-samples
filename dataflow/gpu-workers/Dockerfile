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

FROM tensorflow/tensorflow:2.4.0-gpu

WORKDIR /root

# Installing the requirements here makes the workers start faster since they
# don't need to install the requirements at runtime.
#   ℹ️ Make sure your requirements.txt includes `apache-beam[gcp]`.
COPY requirements.txt .

# Don't install `tensorflow` since the base image already comes with it.
RUN egrep -v '^tensorflow([=<>]|$)' requirements.txt > /tmp/requirements.txt \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

# Copy the Apache Beam required files from the Beam Python SDK image.
COPY --from=apache/beam_python3.6_sdk:2.27.0 /opt/apache/beam /opt/apache/beam

# Set the entrypoint to Apache Beam SDK worker launcher.
ENTRYPOINT [ "/opt/apache/beam/boot" ]
