# Environment variables for system tests.
export GCLOUD_PROJECT=your-project-id
export GCP_PROJECT=$GCLOUD_PROJECT
export GOOGLE_CLOUD_PROJECT=$GCLOUD_PROJECT
export FIRESTORE_PROJECT=

export CLOUD_STORAGE_BUCKET=$GCLOUD_PROJECT
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

# Environment variables for App Engine Flexible system tests.
export GA_TRACKING_ID=
export SQLALCHEMY_DATABASE_URI=sqlite://
export PUBSUB_TOPIC=gae-mvm-pubsub-topic
export PUBSUB_VERIFICATION_TOKEN=1234abc

# Mailgun, Sendgrid, and Twilio config.
# These aren't current used because tests do not exist for these.
export MAILGUN_DOMAIN_NAME=
export MAILGUN_API_KEY=
export SENDGRID_API_KEY=
export SENDGRID_SENDER=
export TWILIO_ACCOUNT_SID=
export TWILIO_AUTH_TOKEN=
export TWILIO_NUMBER=
