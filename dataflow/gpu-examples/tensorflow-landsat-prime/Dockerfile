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

# Each version of TensorFlow requires a specific CUDA/cuDNN version:
#   https://www.tensorflow.org/install/source#gpu
# For a list of all the nvidia images:
#   https://ngc.nvidia.com/catalog/containers/nvidia:cuda/tags
FROM nvcr.io/nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

WORKDIR /pipeline

COPY requirements.txt .
COPY *.py ./

# If you need a different Python version, consider:
#   https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl g++ python3.8-dev python3-distutils \
    && rm -rf /var/lib/apt/lists/* \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.8 10 \
    && curl https://bootstrap.pypa.io/get-pip.py | python \
    # Install the pipeline requirements and check that there are no conflicts.
    # Since the image already has all the dependencies installed,
    # there's no need to run with the --requirements_file option.
    && pip install --no-cache-dir -r requirements.txt \
    && pip check

# Set the entrypoint to Apache Beam SDK worker launcher.
COPY --from=apache/beam_python3.8_sdk:2.38.0 /opt/apache/beam /opt/apache/beam
ENTRYPOINT [ "/opt/apache/beam/boot" ]
