# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

# Configure the Template to launch the pipeline with a --requirements_file option.
# See: https://beam.apache.org/documentation/sdks/python-pipeline-dependencies/#pypi-dependencies
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="/template/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/streaming_beam.py"

COPY . /template

RUN apt-get update \
    # Install any apt packages if required by your template pipeline.
    && apt-get install -y libffi-dev git \
    && rm -rf /var/lib/apt/lists/* \
    # Upgrade pip and install the requirements.
    && pip install --no-cache-dir --upgrade pip \
    # Install dependencies from requirements file in the launch environment.
    && pip install --no-cache-dir -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE \
    # When FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE  option is used,
    # then during Template launch Beam downloads dependencies
    # into a local requirements cache folder and stages the cache to workers.
    # To speed up Flex Template launch, pre-download the requirements cache
    # when creating the Template.
    && pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r $FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE

# Set this if using Beam 2.37.0 or earlier SDK to speed up job submission.
ENV PIP_NO_DEPS=True

ENTRYPOINT ["/opt/google/dataflow/python_template_launcher"]
