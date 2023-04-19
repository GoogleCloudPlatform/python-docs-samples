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

# Environment variables for system tests.
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_PROJECT=$GOOGLE_CLOUD_PROJECT
export GOOGLE_CLOUD_PROJECT_NUMBER=
export FIRESTORE_PROJECT=

export CLOUD_STORAGE_BUCKET=$GOOGLE_CLOUD_PROJECT
export REQUESTER_PAYS_TEST_BUCKET="${CLOUD_STORAGE_BUCKET}-requester-pays-test"
export API_KEY=
export BIGTABLE_CLUSTER=bigtable-test
export BIGTABLE_ZONE=us-central1-c
export BIGTABLE_INSTANCE=
export SPANNER_INSTANCE=
export COMPOSER_LOCATION=us-central1
export COMPOSER_ENVIRONMENT=
export COMPOSER2_ENVIRONMENT=
# Webserver for COMPOSER2_ENVIRONMENT
export COMPOSER2_WEB_SERVER_URL=
export CLOUD_KMS_KEY=

export MYSQL_INSTANCE=
export MYSQL_USER=
export MYSQL_PASSWORD=
export MYSQL_DATABASE=
export MYSQL_HOST=localhost:3306
export MYSQL_INSTANCE_HOST=localhost
export MYSQL_PORT=3306
export MYSQL_UNIX_SOCKET=
export POSTGRES_INSTANCE=
export POSTGRES_USER=
export POSTGRES_PASSWORD=
export POSTGRES_DATABASE=
export POSTGRES_HOST=localhost:5432
export POSTGRES_INSTANCE_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_UNIX_SOCKET=
export SQLSERVER_INSTANCE=
export SQLSERVER_USER=
export SQLSERVER_PASSWORD=
export SQLSERVER_DATABASE=
export SQLSERVER_HOST=127.0.0.1:1433
export DB_SOCKET_DIR=

export KG_API_KEY=
export SLACK_TEST_SIGNATURE=
export SLACK_SECRET=
export FUNCTIONS_TOPIC=

# Service account for HMAC samples
export HMAC_KEY_TEST_SERVICE_ACCOUNT=

# Environment variables for App Engine Flexible system tests.
export GA_TRACKING_ID=
export SQLALCHEMY_DATABASE_URI=sqlite://
export PUBSUB_TOPIC=gae-mvm-pubsub-topic
export PUBSUB_VERIFICATION_TOKEN=1234abc

# Secret Manager Test Vars
export GCLOUD_SECRETS_SERVICE_ACCOUNT=

# Automl
# A centralized project is used to remove duplicate work across all 7 languages 
# and reduce the management of these resources.
# https://docs.google.com/document/d/1-E7zTNqBm9ex7XIOhzMHCupwKWieyMKgAVwrRK5JTVY
export AUTOML_PROJECT_ID=

export ENTITY_EXTRACTION_DATASET_ID=
export ENTITY_EXTRACTION_MODEL_ID=

export SENTIMENT_ANALYSIS_DATASET_ID=
export SENTIMENT_ANALYSIS_MODEL_ID=

export TEXT_CLASSIFICATION_DATASET_ID=
export TEXT_CLASSIFICATION_MODEL_ID=

export TRANSLATION_DATASET_ID=
export TRANSLATION_MODEL_ID=

export VISION_CLASSIFICATION_DATASET_ID=
export VISION_CLASSIFICATION_MODEL_ID=

export OBJECT_DETECTION_DATASET_ID=
# AutoML model takes 8-24 hours to create, having predefined 
# and centralized models remove duplicate work across all languages.
export OBJECT_DETECTION_MODEL_ID=

# For git operations in the test driver(testing/run_tests.sh).
# These are optional, but for avoiding flakes in Kokoro builds.
export GITHUB_ACCESS_TOKEN=
export GITHUB_USERNAME=

# Cloud Run
# For run/idp example, a Firebase IDP token
export IDP_KEY=
# For run/filesystem
export IP_ADDRESS=
export CONNECTOR=

# Dialogflow examples.
export SMART_REPLY_MODEL=
export SMART_REPLY_ALLOWLIST=
