# Copyright 2024 Google LLC
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


# This Dockerfile defines a container image that will serve as both SDK container image
# (launch environment) and the base image for Dataflow Flex Template (launch environment).
#
# For more information, see:
#   - https://cloud.google.com/dataflow/docs/reference/flex-templates-base-images
#   - https://cloud.google.com/dataflow/docs/guides/using-custom-containers

# NOTE: the version of Python interpreter and Beam SDK should be consistent throughout the project.
# Use the same version of apache_beam in setup.py if you add an explicit dependency on Beam.

# Use a custom base image for our containers. This is done as an illustration of possible
# image for possible customizations. A 'slim' base image results in smaller image size,
# but does not include some normally preinstalled libraries, like google-cloud-debugger.
# To use a standard image, use apache/beam_python3.11_sdk:2.54.0 instead.
FROM python:3.11-slim

# Copy SDK entrypoint binary from Apache Beam image, so that we can use our image as SDK container image.
COPY --from=apache/beam_python3.11_sdk:2.54.0 /opt/apache/beam /opt/apache/beam

# Copy flex template launcher binary for the launcher image, so that we can use our image as a Flex Template.
COPY --from=gcr.io/dataflow-templates-base/python311-template-launcher-base:20230622_RC00 /opt/google/dataflow/python_template_launcher /opt/google/dataflow/python_template_launcher

# Location to store the pipeline artifacts.
# The /template folder name is chosen for consistency with the default WORKDIR used
# when template image is created via `gcloud flex-templates build` command.
ARG WORKDIR=/template
WORKDIR ${WORKDIR}

COPY requirements.txt .
COPY setup.py .
COPY main.py .
COPY my_package my_package

# Installing exhaustive list of dependencies from a requirements.txt
# helps to ensure that every time Docker container image is built, the Python dependencies stay the same.
RUN pip install -r requirements.txt

# Installing the pipeline package will make all modules encompassing the pipeline
# to be available via import statements, and make sure all necessary dependencies are installed .
 # Editable installation allows picking up later changes to the pipeline code
# for example during local experimentation within the container, or when the final flex template image is built.
RUN pip install -e .

# For more informaiton, see: https://cloud.google.com/dataflow/docs/guides/templates/configuring-flex-templates
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/main.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"

# To reduce pipeline submission time
# we are not using FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE directive here
# to specify pipeline dependencies, because we will use this image as custom sdk container image
# and it already installs the dependencies from the requirements.txt.

# Optionally, verify that dependencies are not conflicting. A conflict may or may not be significant for your pipeline.
RUN pip check

# Optionally, list all installed dependencies. The output can be used to seed requirements.txt for reproducible builds.
RUN pip freeze

# Set the entrypoint to Apache Beam SDK launcher.
ENTRYPOINT ["/opt/apache/beam/boot"]
