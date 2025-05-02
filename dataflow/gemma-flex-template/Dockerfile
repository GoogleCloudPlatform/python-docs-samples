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

# This uses Ubuntu with Python 3.11 and comes with CUDA drivers for
# GPU use.
ARG SERVING_BUILD_IMAGE=pytorch/pytorch:2.6.0-cuda11.8-cudnn9-runtime

FROM ${SERVING_BUILD_IMAGE}

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends apt-utils curl wget git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && git clone https://github.com/google/gemma_pytorch.git \
    && pip install --no-cache-dir -r requirements.txt ./gemma_pytorch

# Copy SDK entrypoint binary from Apache Beam image, which makes it possible to
# use the image as SDK container image.
# The Beam version should match the version specified in requirements.txt
COPY --from=apache/beam_python3.10_sdk:2.62.0 /opt/apache/beam /opt/apache/beam

# Copy Flex Template launcher binary from the launcher image, which makes it
# possible to use the image as a Flex Template base image.
COPY --from=gcr.io/dataflow-templates-base/python310-template-launcher-base:latest /opt/google/dataflow/python_template_launcher /opt/google/dataflow/python_template_launcher

# Copy the model directory downloaded from Kaggle and the pipeline code.
COPY pytorch_model pytorch_model
COPY custom_model_gemma.py custom_model_gemma.py

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="custom_model_gemma.py"

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]