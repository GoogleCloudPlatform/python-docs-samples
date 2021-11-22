# Copyright 2021 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# [START composer_cicd_add_dags_to_environment_dockerfile]

FROM python:3.10

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True



COPY utils/requirements.txt ./
COPY utils/add_dags_to_composer_environment.py ./

RUN pip install --no-cache-dir -r requirements.txt

#copy dag code to container image
ENV DAGS /dags
WORKDIR $DAGS
COPY . ./
ARG dags_directory
ARG dags_bucket
#TODO change to be templated
# CMD ["python", "add_dags_to_composer.py", "--dags_directory=\"dags/\"", "--dags_bucket=\"leah-playground\""]
CMD ["python", "add_dags_to_composer.py", "--dags_directory=dags_directory", "--dags_bucket=dags_bucket"]

# [END composer_cicd_add_dags_to_environment_dockerfile]
