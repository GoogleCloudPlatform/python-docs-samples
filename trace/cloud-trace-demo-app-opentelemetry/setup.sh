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

echo ################## Set up cloud trace demo application ###########################
kubectl apply -f app/cloud-trace-demo.yaml

echo ""
echo -n "Wait for load balancer initialization complete."
for run in {1..20}
do
  sleep 5
  endpoint=`kubectl get svc cloud-trace-demo-a -ojsonpath='{.status.loadBalancer.ingress[0].ip}'`
  if [[ "$endpoint" != "" ]]; then
    break
  fi
  echo -n "."
done

echo ""
if [ -n "$endpoint" ]; then
  echo "Completed. You can access the demo at http://${endpoint}/"
else
  echo "There is a problem with the setup. Cannot determine the endpoint."
fi
popd
