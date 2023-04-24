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

# -- Builder stage
# https://docs.docker.com/develop/develop-images/multistage-build/
FROM continuumio/miniconda3:22.11.1-alpine AS builder

# Create a virtual environment and make it standalone with conda-pack.
# https://conda.github.io/conda-pack
RUN conda create -y -n env python=3.9 \
    && conda install -y conda-pack \
    && conda-pack -n env -o /tmp/env.tar \
    && mkdir /opt/python \
    && tar -xf /tmp/env.tar -C /opt/python \
    && /opt/python/bin/conda-unpack

# -- Main image
FROM ubuntu:latest

WORKDIR /pipeline

# Set the entrypoint to Apache Beam SDK worker launcher.
COPY --from=apache/beam_python3.9_sdk:2.38.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]

# Copy the python installation from the builder stage.
COPY --from=builder /opt/python /opt/python
ENV PATH /opt/python/bin:${PATH}

# Install the requirements.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip check

# Copy the pipeline source files.
COPY main.py ./
