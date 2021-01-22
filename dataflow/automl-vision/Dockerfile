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

FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG PY_FILE=wildlife-insights.py
ARG WORKDIR=/dataflow/template

RUN apt-get update \
    && apt-get install -y libffi-dev git \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p ${WORKDIR}

WORKDIR ${WORKDIR}

COPY requirements.txt .
COPY ${PY_FILE} .

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/${PY_FILE}}"

RUN pip install -U pip=='20.2.*' \
    && pip install -r requirements.txt
