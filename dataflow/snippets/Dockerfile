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

# NOTE: The KafkaIO connector for Python requires the JRE to be installed
# in the execution environment. This Dockerfile enables the
# "dataflow_kafka_read" snippet to be tested without installing the JRE
# on the host machine. This Dockerfile is derived from the
# dataflow/custom-containers/ubuntu sample.

FROM python:3.12-slim

# Install JRE
COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 10 

WORKDIR /pipeline

# Copy files from official SDK image.
COPY --from=apache/beam_python3.11_sdk:2.63.0 /opt/apache/beam /opt/apache/beam
# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Install Docker.
RUN apt-get update
RUN apt-get install -y --no-install-recommends docker.io

# Install dependencies.
RUN pip3 install --no-cache-dir apache-beam[gcp]==2.63.0
RUN pip install --no-cache-dir kafka-python==2.0.6

# Verify that the image does not have conflicting dependencies.
RUN pip check

# Copy the snippets to test.
COPY read_kafka.py ./
COPY read_kafka_multi_topic.py ./

