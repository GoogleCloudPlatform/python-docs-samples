# Environment variables for system tests.
export GOOGLE_CLOUD_PROJECT=your-project-id
export GCP_PROJECT=$GOOGLE_CLOUD_PROJECT
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
export CLOUD_KMS_KEY=

export MYSQL_INSTANCE=
export MYSQL_USER=
export MYSQL_PASSWORD=
export MYSQL_DATABASE=
export POSTGRES_INSTANCE=
export POSTGRES_USER=
export POSTGRES_PASSWORD=
export POSTGRES_DATABASE=

export KG_API_KEY=
export SLACK_TEST_SIGNATURE=
export SLACK_SECRET=
export FUNCTIONS_TOPIC=

# HMAC SA Credentials for S3 SDK samples
export GOOGLE_CLOUD_PROJECT_S3_SDK=
export STORAGE_HMAC_ACCESS_KEY_ID=
export STORAGE_HMAC_ACCESS_SECRET_KEY=

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
export OBJECT_DETECTION_MODEL_ID=

# For git operations in the test driver(testing/run_tests.sh).
# These are optional, but for avoiding flakes in Kokoro builds.
export GITHUB_ACCESS_TOKEN=
export GITHUB_USERNAME=
