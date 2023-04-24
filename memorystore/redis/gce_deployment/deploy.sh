#!/bin/bash

# Copyright 2018 Google Inc.
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
# [START memorystore_deploy_sh]
if [ -z "$REDISHOST" ]; then
  echo "Must set \$REDISHOST. For example: REDISHOST=127.0.0.1"
  exit 1
fi

if [ -z "$REDISPORT" ]; then
  echo "Must set \$REDISPORT. For example: REDISPORT=6379"
  exit 1
fi

if [ -z "$GCS_BUCKET_NAME" ]; then
  echo "Must set \$GCS_BUCKET_NAME. For example: GCS_BUCKET_NAME=my-bucket"
  exit 1
fi

if [ -z "$ZONE" ]; then
  ZONE=$(gcloud config get-value compute/zone -q)
  echo $ZONE
fi

#Upload the tar to GCS
tar -cvf app.tar -C .. requirements.txt main.py
# Copy to GCS bucket
gsutil cp app.tar gs://"$GCS_BUCKET_NAME"/gce/

# Create an instance
gcloud compute instances create my-instance \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --machine-type=g1-small \
    --scopes cloud-platform \
    --metadata-from-file startup-script=startup-script.sh \
    --metadata gcs-bucket=$GCS_BUCKET_NAME,redis-host=$REDISHOST,redis-port=$REDISPORT \
    --zone $ZONE \
    --tags http-server

gcloud compute firewall-rules create allow-http-server-8080 \
    --allow tcp:8080 \
    --source-ranges 0.0.0.0/0 \
    --target-tags http-server \
    --description "Allow port 8080 access to http-server"
# [END memorystore_deploy_sh]
