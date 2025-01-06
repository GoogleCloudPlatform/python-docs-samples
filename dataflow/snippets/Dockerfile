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

FROM ubuntu:focal

WORKDIR /pipeline

COPY --from=apache/beam_python3.11_sdk:2.61.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]

COPY requirements.txt .
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl python3-distutils default-jre docker.io \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3 10 \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    # Install the requirements.
    && pip install --no-cache-dir -r requirements.txt \
    && pip check


COPY read_kafka.py ./
COPY read_kafka_multi_topic.py ./
