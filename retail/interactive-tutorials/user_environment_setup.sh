#!/bin/bash

# Copyright 2022 Google LLC
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

success() {
    echo "========================================="
    echo "The Google Cloud setup is completed."
    echo "Please proceed with the Tutorial steps"
    echo "========================================="
    exit 0
}

failure() {
    echo "========================================="
    echo "The Google Cloud setup was not completed."
    echo "Please fix the errors above!"
    echo "========================================="
    exit 1
}

# catch any error that happened during execution
trap 'failure' ERR

# set the Google Cloud Project ID
project_id=$1
echo "Project ID: $project_id"
gcloud config set project "$project_id"

email=$(gcloud auth list --filter="status:ACTIVE account:$project_id.iam.gserviceaccount.com" --format="value(account)")
echo $email

# Check if user has service account active
if [ -z "$email" ]
then
    # Create a new service account
    timestamp=$(date +%s)
    service_account_id="service-acc-$timestamp"
    echo "Service Account: $service_account_id"
    gcloud iam service-accounts create "$service_account_id"
else
    service_account_id="${email%@*}"
    # Log out of service account
    gcloud auth revoke 2>/dev/null
fi
echo "$service_account_id"


editor=$(gcloud projects get-iam-policy $project_id  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:$service_account_id ROLE=roles/editor")

retail_admin=$(gcloud projects get-iam-policy $project_id  \
--flatten="bindings[].members" \
--format='table(bindings.role)' \
--filter="bindings.members:$service_account_id ROLE=roles/retail.admin")


# Check if any of the needed roles is missing
if [ -z "$editor" ] || [ -z "$retail_admin" ]
then
    # Assign necessary roles to your new service account.
    for role in {retail.admin,editor}
    do
        gcloud projects add-iam-policy-binding "$project_id" --member="serviceAccount:$service_account_id@$project_id.iam.gserviceaccount.com" --role=roles/"${role}"
    done
    echo "Wait ~60 seconds to be sure the appropriate roles have been assigned to your service account"
    sleep 60
fi

# Upload your service account key file.
service_acc_email="$service_account_id@$project_id.iam.gserviceaccount.com"
gcloud iam service-accounts keys create ~/key.json --iam-account "$service_acc_email"

# Activate the service account using the key.
gcloud auth activate-service-account --key-file ~/key.json

'success'
