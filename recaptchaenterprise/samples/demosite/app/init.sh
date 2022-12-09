#!/usr/bin/env bash

# gcloud command to get the current GOOGLE Project id.
export GOOGLE_CLOUD_PROJECT=$(gcloud config list --format 'value(core.project)' 2>/dev/null)
gcloud config set project "$GOOGLE_CLOUD_PROJECT"

# Enabling the reCAPTCHA Enterprise API
gcloud services enable recaptchaenterprise.googleapis.com

# gcloud command to create reCAPTCHA keys.
gcloud alpha recaptcha keys create --display-name=demo-recaptcha-score-key --web --allow-all-domains --integration-type=SCORE 1>/dev/null 2>recaptchascorekeyfile
export SITE_KEY=$(cat recaptchascorekeyfile | sed -n -e 's/.*Created \[\([0-9a-zA-Z_-]\+\)\].*/\1/p')
gcloud alpha recaptcha keys create --display-name=demo-recaptcha-checkbox-key --web --allow-all-domains --integration-type=CHECKBOX 1>/dev/null 2>recaptchacheckboxkeyfile
export CHECKBOX_SITE_KEY=$(cat recaptchacheckboxkeyfile | sed -n -e 's/.*Created \[\([0-9a-zA-Z_-]\+\)\].*/\1/p')

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