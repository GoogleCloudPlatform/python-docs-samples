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

# Make sure the CUDA and cuDNN versions are compatible with your TensorFlow version.
#   https://www.tensorflow.org/install/source#gpu
# Check the Nvidia container registry catalog to look at the available Nvidia images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda
FROM nvidia/cuda:11.3.1-cudnn8-runtime-ubuntu20.04

# The Python version of the Dockerfile MUST match the Python version you use
# to launch the Dataflow job.
ARG python_version=3.8

WORKDIR /root

# Copy the Apache Beam worker files and the requirements.txt file.
COPY --from=apache/beam_python3.8_sdk:2.30.0 /opt/apache/beam /opt/apache/beam
COPY requirements.txt .

# Update PATH so we find our new Conda and Python installations.
ENV PATH=/opt/python/bin:/opt/conda/bin:$PATH

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/* \
    # The nvidia image doesn't come with Python pre-installed.
    # We use Miniconda to install the Python version of our choice.
    && wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && sh Miniconda3-latest-Linux-x86_64.sh -b -p /opt/conda \
    && rm Miniconda3-latest-Linux-x86_64.sh \
    # Create a new Python environment and install our requirements.
    # We don't need to update $PATH since /usr/local is already in $PATH.
    && conda create -y -p /opt/python python=$python_version pip \
    && pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir -r requirements.txt \
    && conda clean -y --all --force-pkgs-dirs \
    # Beam workers looks for pip at /usr/local/bin/pip by default.
    # This can be omitted in Beam 2.30.0 and later versions.
    && ln -s $(which pip) /usr/local/bin/pip

# Set the entrypoint to Apache Beam SDK worker launcher.
ENTRYPOINT [ "/opt/apache/beam/boot" ]
