# Environment variables for system tests.
export GCLOUD_PROJECT=your-project-id
export CLOUD_STORAGE_BUCKET=$GCLOUD_PROJECT
export API_KEY=
export BIGTABLE_CLUSTER=bigtable-test
export BIGTABLE_ZONE=us-central1-c
export SPANNER_INSTANCE=

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
