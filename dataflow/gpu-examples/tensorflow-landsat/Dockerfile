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

# NVIDIA CUDA container: https://catalog.ngc.nvidia.com/orgs/nvidia/containers/cuda
# Supported NVIDIA images: https://gitlab.com/nvidia/container-images/cuda/blob/master/doc/supported-tags.md
# TensorFlow/CUDA compatibility: https://www.tensorflow.org/install/source#gpu
FROM nvcr.io/nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

WORKDIR /pipeline

COPY requirements.txt .
COPY *.py ./

RUN apt-get update \
    # Install Python and other system dependencies.
    && apt-get install -y --no-install-recommends \
        curl g++ python3.10-dev python3-pip python3-distutils \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 10 \
    # Install the pipeline requirements.
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip check

# Set the entrypoint to Apache Beam SDK worker launcher.
# Check this matches the apache-beam version in the requirements.txt
COPY --from=apache/beam_python3.10_sdk:2.46.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]
