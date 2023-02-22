#!/usr/bin/env bash
# Copyright 2023 Google LLC
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

# gcloud command to get the current GOOGLE Project id.
export GOOGLE_CLOUD_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# Enabling the reCAPTCHA Enterprise API
gcloud services enable recaptchaenterprise.googleapis.com

# gcloud command to create reCAPTCHA keys.
gcloud alpha recaptcha keys create --display-name=demo-recaptcha-score-key --web --allow-all-domains --integration-type=SCORE 1>/dev/null 2>recaptchascorekeyfile
export SITE_KEY=$(cat recaptchascorekeyfile | sed -n -e 's/.*Created \[\([0-9a-zA-Z_-]\+\)\].*/\1/p')

# Docker compose up
DOCKER_COMPOSE="/usr/local/bin/docker-compose -f $HOME/cloudshell_open/python-recaptcha-enterprise/samples/demosite/docker-compose.yaml up --build"
$DOCKER_COMPOSE
DOCKER_COMPOSE_RESULT=$?
if [[ $DOCKER_COMPOSE_RESULT == *"error"* ]];
then
  echo "Setting CloudSdk to Python2 due to gcloud openssl issue"
  export CLOUDSDK_PYTHON=python2
  $DOCKER_COMPOSE
fi