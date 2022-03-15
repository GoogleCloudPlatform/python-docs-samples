#!/bin/bash

# Copyright 2022 Google Inc. All Rights Reserved.
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

# get the project_id from gcloud config
project_id=$(gcloud config get-value project)
echo $project_id
timestamp=$(date +%s)
echo $timestamp
service_account_id="service-acc-"$timestamp

# create service account (your project_id+timestamp)
gcloud iam service-accounts create $service_account_id

# assign needed roles to your new service account
for role in {retail.admin,storage.admin,bigquery.admin}
  do
    gcloud projects add-iam-policy-binding $project_id --member="serviceAccount:"$service_account_id"@"$project_id".iam.gserviceaccount.com" --role="roles/${role}"
  done

# upload your service account key file
service_acc_email=$service_account_id"@"$project_id".iam.gserviceaccount.com"
gcloud iam service-accounts keys create ~/key.json --iam-account $service_acc_email

# activate the service account using the key
gcloud auth activate-service-account --key-file ~/key.json

# set the key as GOOGLE_APPLICATION_CREDENTIALS
export GOOGLE_APPLICATION_CREDENTIALS=~/key.json

# install needed Google client libraries
virtualenv -p python3 myenv
source myenv/bin/activate

pip install google
pip install google-cloud-retail
pip install google-cloud.storage
pip install google-cloud.bigquery

echo "Your working environment is set up now!"