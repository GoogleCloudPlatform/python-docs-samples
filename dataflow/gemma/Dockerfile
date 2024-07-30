#  Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This uses Ubuntu with Python 3.11
# You can check the Python version for a given tensorflow
# container at https://hub.docker.com/r/tensorflow/tensorflow/tags
ARG SERVING_BUILD_IMAGE=tensorflow/tensorflow:2.16.1-gpu

FROM ${SERVING_BUILD_IMAGE}

WORKDIR /workspace

RUN apt-get update -y && apt-get install -y \
    cmake

COPY requirements.txt requirements.txt
RUN pip install --upgrade --no-cache-dir pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy files from official SDK image, including script/dependencies.
COPY --from=apache/beam_python3.11_sdk:2.54.0 /opt/apache/beam /opt/apache/beam

# Copy the model directory downloaded from Kaggle and the pipeline code.
COPY gemma_2b gemma_2B
COPY custom_model_gemma.py custom_model_gemma.py

ENV KERAS_BACKEND="tensorflow"

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]