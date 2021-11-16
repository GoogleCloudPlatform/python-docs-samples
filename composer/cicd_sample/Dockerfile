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
# [START composer_cicd_unittest_dockerfile]

FROM python:3.9

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED True

COPY requirements.txt ./
COPY requirements-test.txt ./
COPY constraints.txt ./

# Airflow requires the use of a constraints file for proper pip installation
# See http://airflow.apache.org/docs/apache-airflow/stable/installation/installing-from-pypi.html

RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt
RUN pip install --no-cache-dir -r requirements-test.txt

#copy dag code to container image
ENV DAGS /dags
WORKDIR $DAGS
COPY . ./
CMD ["pytest", "-s", "dags/example_dag_test.py"]
# [END composer_cicd_unittest_dockerfile]
