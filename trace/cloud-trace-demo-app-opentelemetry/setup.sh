#!/bin/bash
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -o errexit  # exit on error
SCRIPT_DIR=$(realpath $(dirname "$0"))
pushd $SCRIPT_DIR > /dev/null

echo ################## Build the demo application image ###########
project_id=${1:-$PROJECT_ID}
if [ -z "$project_id" ]; then
  project_id=$(gcloud config get-value core/project)
fi
if [ -z "$project_id" ]; then
  echo "  Cannot find GCP project id. Please, setup project using 'gcloud config set project' CLI"
  popd
  exit 1
fi

docker build -t gcr.io/${project_id}/cloud-trace-demo:v1 -f app/Dockerfile ./app/

echo ################## Set up service a ###########################
kubectl apply -f app/demo-service-a.yaml

echo ################## Set up service b ###########################
endpoint=""
for run in {1..20}
do
  echo "  Attempt #${run} to fetch the external IP of service a..."
  sleep 5
  endpoint=`kubectl get svc cloud-trace-demo-a -ojsonpath='{.status.loadBalancer.ingress[0].ip}'`
  if [[ "$endpoint" != "" ]]; then
    break
  fi
done

if [[ "$endpoint" == "" ]]; then
  echo "  Unable to get external IP for service cloud-trace-demo-a"
  popd
  exit 1
fi

echo "  Passing external IP for the first service ${endpoint} to the second service template"
sed "s/{{ endpoint }}/${endpoint}/g" app/demo-service-b.yaml.template > app/demo-service-b.yaml
kubectl apply -f app/demo-service-b.yaml
rm app/demo-service-b.yaml

echo ################## Set up service c ###########################
endpoint=""
for run in {1..20}
do
  echo "  Attempt #${run} to fetch the external IP of service b..."
  sleep 5
  endpoint=`kubectl get svc cloud-trace-demo-b -ojsonpath='{.status.loadBalancer.ingress[0].ip}'`
  if [[ "$endpoint" != "" ]]; then
    break
  fi
done

if [[ "$endpoint" == "" ]]; then
  echo "  Unable to get external IP for service cloud-trace-demo-a"
  popd
  exit 1
fi

echo "  Passing external IP for the service b ${endpoint} to the service c"
sed "s/{{ endpoint }}/${endpoint}/g" app/demo-service-c.yaml.template > app/demo-service-c.yaml
kubectl apply -f app/demo-service-c.yaml
rm app/demo-service-c.yaml

echo "  Successfully deployed all services"
popd