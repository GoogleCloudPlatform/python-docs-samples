#!/bin/bash
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

# Postcreate script for Cloud Run button

export SECRET_NAME="idp-sql-secrets"
export SERVICE_ACCOUNT="idp-sql-identity"

# Update Cloud Run service to include Cloud SQL instance, Secret Manager secret,
# and service account
gcloud beta run services update ${K_SERVICE} \
    --platform managed \
    --region ${GOOGLE_CLOUD_REGION} \
    --service-account ${SERVICE_ACCOUNT}@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
    --add-cloudsql-instances ${GOOGLE_CLOUD_PROJECT}:${GOOGLE_CLOUD_REGION}:${CLOUD_SQL_INSTANCE_NAME} \
    --update-secrets CLOUD_SQL_CREDENTIALS_SECRET=${SECRET_NAME}:latest
