# Copyright 2021 Google LLC
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

FROM python:3.9.7

RUN pip3 install --upgrade pip

RUN apt-get update \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

WORKDIR /app
RUN pip3 install -r requirements.txt

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENTRYPOINT ["python"]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 main:app
